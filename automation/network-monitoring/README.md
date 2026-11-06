# Mason–Troy Cisco Monitoring and Evidence Collection

A read-only Python network monitoring and evidence collection tool developed for the Mason–Troy Enterprise Network capstone project.

The script uses **Python, Netmiko, and SSH** to connect to physical Cisco devices, execute monitoring commands, and automatically save timestamped results.

The script does not modify device configurations, store passwords, or automatically collect running configurations.

## 1. Project Overview

The monitoring system provides centralized management and operational visibility across the Mason and Troy network infrastructure.

### Monitored Devices

| Device | Management IP | Role |
|---|---|---|
| MASON-R1 | 10.10.10.1 | Mason router, inter-VLAN routing, and intersite OSPF |
| MASON-SW1 | 10.10.10.2 | Mason Layer 2 switch |
| TROY-SW1 | 10.20.10.1 | Troy Layer 3 switch and OSPF routing |

The monitoring script runs from a Windows desktop connected to the Mason management VLAN.

## 2. Requirements

- Python 3.10 or newer
- Netmiko 4.8.0
- Paramiko 3.5.1
- SSH connectivity to the Cisco devices
- Authorized local administrator credentials
- Network access permitted by device management ACLs

### Install Dependencies

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Install the required libraries:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The `requirements.txt` file specifies:

```text
netmiko==4.8.0
paramiko==3.5.1
```

These versions were successfully tested with the physical Cisco equipment.

## 3. Network Management Requirements

The monitoring computer must have connectivity to the Cisco management interfaces.

The Mason management network uses:

- Network: `10.10.10.0/24`
- Router gateway: `10.10.10.1`
- Mason switch: `10.10.10.2`

The monitoring desktop was configured with the management address `10.10.10.50`.

Access to TROY-SW1 requires routing to `10.20.10.0/24` through MASON-R1.

The management ACLs restrict SSH access to authorized networks. MASON-R1 also permits the designated Troy emergency management address `10.20.10.5`; this exception does not grant access to MASON-SW1.

### Windows Routing Consideration

During testing, Windows initially preferred the desktop's normal Wi-Fi default gateway instead of the Mason management gateway.

A specific route was added:

```powershell
route add 10.20.10.0 mask 255.255.255.0 10.10.10.1 metric 1 IF 12
```

Interface 12 was the USB-to-Ethernet adapter on the test desktop. This interface number is machine-specific and must be verified before reusing the command.

After correcting the route, the desktop successfully reached the Troy management network.

## 4. Running the Monitoring Script

The project includes:

```text
network-monitoring/
├── network_monitor.py
├── devices.json
├── requirements.txt
└── README.md
```

Confirm that `devices.json` contains the correct device addresses.

Run the monitoring script from the project directory:

```powershell
.\.venv\Scripts\python.exe network_monitor.py --inventory devices.json
```

The script prompts for SSH usernames and passwords as needed.

Passwords are entered interactively and are not intentionally written to evidence files.

Each monitoring run creates a timestamped directory:

```text
evidence/
└── YYYYMMDD_HHMMSS_offset/
    ├── MASON-R1/
    ├── MASON-SW1/
    ├── TROY-SW1/
    └── summary.json
```

## 5. Automated Monitoring Commands

The script executes device-specific Cisco IOS `show` commands.

### Common Commands

- `show clock`
- `show version`
- `show ip interface brief`
- `show ip ssh`
- `show logging`

### Routing Commands

Collected from MASON-R1 and TROY-SW1:

- `show ip route`
- `show ip ospf neighbor`
- `show ip protocols`

MASON-R1 also collects:

- `show interfaces GigabitEthernet0/1`

### Switching Commands

Collected from MASON-SW1 and TROY-SW1:

- `show vlan brief`
- `show interfaces trunk`
- `show port-security`
- `show interfaces counters errors`

The script distinguishes Layer 2 and Layer 3 devices to avoid sending unsupported routing commands to MASON-SW1.

## 6. Legacy SSH Compatibility

The physical Cisco devices use older IOS software with limited SSH algorithm support.

During initial testing, modern Windows OpenSSH and Paramiko 5.1.0 could not negotiate compatible SSH algorithms.

Observed compatibility issues included:

- Legacy Diffie-Hellman key exchange
- `ssh-rsa` host key signatures
- CBC encryption ciphers
- SHA-1 message authentication algorithms

### Resolution

A dedicated Python virtual environment was created using:

- Netmiko 4.8.0
- Paramiko 3.5.1

This combination successfully authenticated to all three Cisco devices.

**Security consideration:** These older SSH algorithms are not recommended for production environments. Their use is limited to the isolated capstone management network. Upgrading to equipment or IOS versions supporting modern cryptography remains a future security improvement.

## 7. Automation Validation — November 6, 2026

The monitoring script was successfully executed against all three physical Cisco devices.

### Validation Results

| Device | SSH Authentication | Commands Collected | Result |
|---|---|---|---|
| MASON-R1 | Successful | 9/9 | Pass |
| MASON-SW1 | Successful | 9/9 | Pass |
| TROY-SW1 | Successful | 12/12 | Pass |
| **Total** | **3/3 devices** | **30/30** | **Pass** |

### Validated Capabilities

- Authenticated SSH connections to all three Cisco devices
- Automated execution of device-specific monitoring commands
- Retrieval of interface, routing, VLAN, SSH, and logging information
- Generation of timestamped evidence files
- Generation of structured JSON monitoring summaries
- Detection and reporting of unsupported commands
- Graceful handling of unreachable devices
- Interactive credential handling without intentionally storing passwords

All 30 monitoring commands returned a `collected` status in the generated JSON summary.

**Validation evidence:** `evidence/20261106_124923_-0500/summary.json` was generated locally during the successful test.

The full automation test demonstrates centralized network monitoring and evidence collection across the Mason and Troy infrastructure.

Command collection success does not independently confirm the operational health or security enforcement of every network component.

## 8. Security and Limitations

The script is designed for read-only monitoring.

It does not:

- Modify device configurations
- Automatically remediate security problems
- Collect complete running configurations
- Store SSH passwords
- Prove unauthorized SSH attempts are blocked
- Prove port-security violations are enforced
- Prove OT isolation ACLs block prohibited traffic

Those security controls require separate operational validation.

The `show logging` output may contain usernames, management IP addresses, or other operational information. Evidence must be reviewed before public publication.

Do not commit Python virtual environments, private credentials, password hashes, or unreviewed raw logs to GitHub.

## 9. Capstone Significance

This automation component demonstrates the practical use of Python and Netmiko for centralized enterprise network administration.

Rather than manually connecting to each Cisco device and executing monitoring commands, an administrator can collect consistent information across multiple network devices from a single workstation.

The implementation also demonstrates troubleshooting involving SSH algorithm compatibility, Windows routing, VLAN management interfaces, and device-specific Cisco IOS commands.

**Project status: Successfully implemented and validated across all three physical Cisco devices on November 6, 2026.**