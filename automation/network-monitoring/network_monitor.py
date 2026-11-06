#!/usr/bin/env python3
"""Mason–Troy Cisco network evidence collector (read-only).

Install: python -m pip install -r requirements.txt
Run:     python network_monitor.py --inventory devices.json

Only issues show commands. Credentials are prompted, not persisted.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import getpass
import json
from pathlib import Path
import re
import socket
import sys
import time

try:
    from netmiko import ConnectHandler
except ImportError:
    sys.exit("Netmiko is missing. Install with: python -m pip install netmiko")

DEFAULT_COMMANDS = [
    "show clock",
    "show version",
    "show ip interface brief",
    "show ip ssh",
    "show logging",
]
SWITCH_COMMANDS = [
    "show vlan brief",
    "show interfaces trunk",
    "show port-security",
    "show interfaces counters errors",
]
ROUTER_COMMANDS = [
    "show ip route",
    "show ip ospf neighbor",
    "show ip protocols",
    "show interfaces GigabitEthernet0/1",
    ]
# Never collect running-config, usernames, secrets, or password hashes automatically.
DANGEROUS = re.compile(r"(?:show\s+(?:run|running-config|startup-config)|debug|configure|copy|reload|write|clear|delete|erase|terminal\s+monitor)", re.I)
ERROR_LINES = ("% Invalid input", "% Ambiguous command", "% Incomplete command", "% Unrecognized command", "% Unknown command")


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("._") or "device"


def check_port(host: str, port: int, timeout: float = 3) -> tuple[bool, str]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, "TCP connection succeeded"
    except OSError as exc:
        return False, f"TCP connection failed: {exc}"


def collect_one(device: dict, base_dir: Path, timeout: int, username: str | None) -> dict:
    name, host = device["name"], device["host"]
    kind = device.get("kind", "switch")
    commands = list(DEFAULT_COMMANDS)
    commands += ROUTER_COMMANDS if kind == "router" else SWITCH_COMMANDS
    commands.extend(device.get("extra_commands", []))
    # De-duplicate without changing order and refuse commands other than show.
    commands = list(dict.fromkeys(commands))
    for command in commands:
        if not re.fullmatch(r"show\s+[\w\s./:-]+", command, re.I) or DANGEROUS.search(command):
            raise ValueError(f"Unsafe/unsupported evidence command for {name}: {command!r}")

    device_dir = base_dir / slug(name)
    device_dir.mkdir(parents=True, exist_ok=True)
    report = {"name": name, "host": host, "kind": kind, "ssh_tcp": None, "ssh": "not attempted", "commands": []}
    reachable, detail = check_port(host, int(device.get("port", 22)))
    report["ssh_tcp"] = {"reachable": reachable, "detail": detail}
    if not reachable:
        report["ssh"] = "skipped: SSH TCP port unreachable (check VLAN, routes, VTY ACL, and SSH service)"
        return report

    user = device.get("username") or username
    if not user:
        user = input(f"SSH username for {name} ({host}): ").strip()
    password = getpass.getpass(f"SSH password for {user}@{name}: ")
    connection_args = {
        "device_type": "cisco_ios", "host": host, "port": int(device.get("port", 22)),
        "username": user, "password": password, "conn_timeout": timeout,
        "auth_timeout": timeout, "banner_timeout": timeout,
        "fast_cli": False,
    }
    if device.get("secret_required", False):
        connection_args["secret"] = getpass.getpass(f"Enable secret for {name}: ")
    # Don't preserve credentials in logs or result dictionaries.
    del password
    try:
        with ConnectHandler(**connection_args) as session:
            if device.get("secret_required", False):
                session.enable()
            report["ssh"] = "authenticated"
            for index, command in enumerate(commands, start=1):
                started = time.monotonic()
                print(f"    [{index}/{len(commands)}] {command}", flush=True)
                try:
                    output = session.send_command(command, read_timeout=timeout, strip_prompt=True, strip_command=True)
                    failure = next((line for line in ERROR_LINES if line in output), None)
                    status = "unsupported/error" if failure else "collected"
                    filename = f"{index:02d}_{slug(command)}.txt"
                    (device_dir / filename).write_text(f"Device: {name}\nCommand: {command}\nUTC: {datetime.now(timezone.utc).isoformat()}\n\n{output}\n", encoding="utf-8")
                    report["commands"].append({"command": command, "status": status, "file": str((Path(slug(name)) / filename)), "seconds": round(time.monotonic() - started, 2)})
                except Exception as exc:
                    report["commands"].append({"command": command, "status": "error", "error": f"{type(exc).__name__}: {exc}"})
    except Exception as exc:
        report["ssh"] = f"failed: {type(exc).__name__}: {exc}"
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=Path("devices.json"))
    parser.add_argument("--output", type=Path, default=Path("evidence"))
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--username", help="Fallback SSH username; secrets are always prompted")
    args = parser.parse_args()
    try:
        inventory = json.loads(args.inventory.read_text(encoding="utf-8"))
        devices = inventory["devices"]
        if not isinstance(devices, list) or not devices:
            raise ValueError("'devices' must be a nonempty list")
        for item in devices:
            if not all(isinstance(item.get(k), str) and item[k].strip() for k in ("name", "host")):
                raise ValueError("each device needs nonempty name and host strings")
            if item.get("kind", "switch") not in ("router", "switch"):
                raise ValueError("device kind must be 'router' or 'switch'")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        sys.exit(f"Inventory problem: {exc}")

    stamp = datetime.now().astimezone().strftime("%Y%m%d_%H%M%S_%z")
    base_dir = args.output / stamp
    base_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for item in devices:
        print(f"\nCollecting {item['name']} ({item['host']}) ...", flush=True)
        try:
            result = collect_one(item, base_dir, args.timeout, args.username)
        except Exception as exc:
            result = {"name": item["name"], "host": item["host"], "ssh": f"error: {type(exc).__name__}: {exc}", "commands": []}
        results.append(result)
        print(f"  SSH result: {result['ssh']}", flush=True)

    summary = {"collection_time_local": stamp, "note": "Read-only configuration/operational snapshots; config != enforcement validation", "devices": results}
    (base_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nEvidence written to: {base_dir.resolve()}")
    print("Review logs for network details before sharing publicly; no passwords are intentionally collected.")
    return 0 if all(x["ssh"] == "authenticated" for x in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
