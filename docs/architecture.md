# Network Architecture



This document describes the physical and virtual architecture of the Mason-Troy Enterprise Network and how the two locations communicate.



## Overall Design



The project represents a two-site enterprise and manufacturing environment consisting of:



- **Mason, Ohio — Corporate Headquarters**

- **Troy, Ohio — Manufacturing Facility**



The sites are connected through a routed point-to-point WAN. OSPF Area 0 provides dynamic route exchange between the locations.



Mason uses router-on-a-stick inter-VLAN routing through MASON-R1, while Troy uses Layer 3 switching on TROY-SW1. This design demonstrates two different methods of providing inter-VLAN routing within the same enterprise environment.



## Mason Architecture



Mason serves as the corporate headquarters and hosts the project's primary server and network service infrastructure.



### Network Components



- **MASON-R1 — Cisco 2901**

   - Provides router-on-a-stick inter-VLAN routing.

   - Acts as the Mason endpoint of the routed WAN.

   - Advertises Mason networks into OSPF.

   - Provides the upstream path toward the FortiGate security edge and Internet.



- **MASON-SW1 — Cisco Catalyst 3560**

   - Operates as a Layer 2 access switch.

   - Provides VLAN connectivity for management, employee, and server networks.

   - Uses an 802.1Q trunk to MASON-R1.

   - Uses an additional 802.1Q trunk to connect physical VLANs with the GNS3 virtual environment.



- **Windows Server 2025**
  - Located in Mason VLAN 30 at `10.10.30.10`.
  - Hosts Active Directory Domain Services for `masonmfg.internal`.
  - Provides centralized DNS for Mason and Troy.
  - Hosts the `CompanyShare` SMB shared folder.
  - Uses Active Directory security groups and NTFS/share permissions to control shared-resource access.
  - Provides centralized Group Policy management for domain-joined Windows workstations.
  - Records Windows Security events for authentication, Kerberos activity, and other configured audit categories.
  - Successfully authenticated a Troy domain user accessing shared resources across the routed WAN.



- **Ubuntu Server**

   - Located in Mason VLAN 30.

   - Provides centralized Kea DHCP and other Linux-based infrastructure services.




- **MASON-WIN11-01 — Windows 11 Pro Workstation**
  - Located in Mason VLAN 20 — Employees.
  - Receives IP configuration from the centralized Kea DHCP server.
  - Joined to the `masonmfg.internal` Active Directory domain.
  - Computer account resides in `MasonMFG → Mason → Computers`.
  - Uses `MASONMFG\test.manager` for domain authentication testing.
  - Receives the Domain Workstation Security Baseline through Group Policy.
  - Provides a Mason-side endpoint for validating centralized authentication, security policies, and enterprise connectivity.



### Mason VLANs



- VLAN 10 — Management

- VLAN 20 — Employees

- VLAN 30 — Servers

- VLAN 999 — Native VLAN



## Troy Architecture



Troy represents the manufacturing facility and contains both standard business systems and the legacy manufacturing environment.



### Network Components



- **TROY-SW1 — Cisco Catalyst 3560**

   - Operates as a Layer 3 switch.

   - Provides the default gateways for Troy VLANs using switched virtual interfaces (SVIs).

   - Performs inter-VLAN routing.

   - Acts as the Troy endpoint of the routed WAN.

   - Participates directly in OSPF Area 0 with MASON-R1.



- **Employee Systems**

   - Located in VLAN 20.

   - Provide normal business connectivity at the manufacturing facility.

   - TROY-WIN11-01 provides the current Windows 11 enterprise client used for DHCP, Active Directory, Group Policy, DNS, and routed connectivity validation.

   - TROY-WIN11-01 receives centralized DHCP service from the Mason Ubuntu Server through DHCP relay on TROY-SW1.





- **Legacy Windows XP Manufacturing System**

   - Located in VLAN 30 — Legacy/OT.

   - Represents an older system that remains necessary for manufacturing operations.

- The legacy Windows XP manufacturing endpoint is assigned to Troy VLAN 30 (`10.20.30.0/24`).
- TROY-SW1 enforces bidirectional routed isolation using extended ACLs:
  - `TROY-OT-IN` restricts traffic originating from the Legacy/OT VLAN.
  - `TROY-OT-OUT` restricts routed traffic entering the Legacy/OT VLAN.
- Before-and-after connectivity tests confirmed that the ACLs restrict communication between the Legacy/OT network and other routed enterprise networks.
- ACL deny counters increased during controlled testing, providing evidence of enforcement.
- Devices within the same Legacy/OT VLAN can still communicate locally through Layer 2 switching.
- DHCP functionality was validated before ACL deployment; DHCP operation after applying the ACLs remains unverified.
- The isolation design limits the legacy environment's exposure to other enterprise networks and external destinations.


### Troy Switch Security Hardening

TROY-SW1 implements additional Layer 2 and management-plane security controls to protect the manufacturing network.

- **Port security:** Configured on 12 access ports, allowing a maximum of one learned MAC address per port with violation mode set to `restrict`.
- **PortFast:** Enabled on designated access ports to allow connected endpoints to transition promptly into forwarding.
- **BPDU Guard:** Configured on designated access ports to protect against unexpected spanning-tree participation.
- **SSH management:** SSH version 2 is enabled for encrypted remote administration.
- **Web management:** HTTP and HTTPS management services are disabled.

Configuration and operational checks confirmed these controls were enabled.

Unauthorized MAC address enforcement, BPDU Guard violation behavior, and Telnet rejection were not independently tested. These remain validation opportunities rather than confirmed behavioral results.

Supporting configuration and verification screenshots are documented in [Validation Evidence](validation.md).


### Troy VLANs



- VLAN 10 — Management

- VLAN 20 — Employees

- VLAN 30 — Legacy/OT

- VLAN 999 — Native VLAN



## WAN and Dynamic Routing



Mason and Troy are connected using a routed point-to-point WAN network.



### WAN Addressing



- Network: `10.255.0.0/30`

- MASON-R1: `10.255.0.1`

- TROY-SW1: `10.255.0.2`



### OSPF



OSPF process 1 and Area 0 are used to dynamically exchange routes between the two sites.

MASON-R1 also advertises its default route into OSPF. TROY-SW1 learns `0.0.0.0/0` through MASON-R1 at `10.255.0.1`, providing Troy with a dynamically learned path toward the centralized FortiGate Internet edge.



MASON-R1 advertises:



- `10.10.10.0/24` — Mason Management

- `10.10.20.0/24` — Mason Employees

- `10.10.30.0/24` — Mason Servers

- `10.255.0.0/30` — WAN



TROY-SW1 advertises:



- `10.20.10.0/24` — Troy Management

- `10.20.20.0/24` — Troy Employees

- `10.20.30.0/24` — Troy Legacy/OT

- `10.255.0.0/30` — WAN



A full OSPF adjacency has been established between MASON-R1 and TROY-SW1. Bidirectional route propagation has been validated, allowing both sites to dynamically learn the remote site's networks.



## Physical and Virtual Network Integration



The project combines physical Cisco infrastructure with virtual systems hosted in GNS3.



At Mason, virtual servers connect to a GNS3 Ethernet switch configured with access ports for the appropriate VLANs. The virtual switch uses an 802.1Q trunk to a GNS3 Cloud interface, which bridges the virtual network to a physical USB-to-Ethernet adapter on the virtualization host.



The USB-to-Ethernet adapter connects to MASON-SW1 Fa0/5, which is configured as an 802.1Q trunk carrying VLANs 10, 20, 30, and 999.



### Virtual-to-Physical Traffic Path



For a virtual server in Mason VLAN 30, the traffic path is:



`Virtual Server → GNS3 Ethernet Switch → GNS3 Cloud → USB-to-Ethernet Adapter → MASON-SW1 → MASON-R1`



This design allows virtual systems to participate directly in the same VLAN and routing infrastructure as the physical Cisco equipment.



### Current Virtual Switch Layout



- Ports 2–3 — Access VLAN 10

- Ports 5–7 — Access VLAN 20

- Ports 9–11 — Access VLAN 30

- Port 12 — 802.1Q trunk toward the physical Mason network



Windows Server 2025 currently connects through port 9, and Ubuntu Server connects through port 10. Both systems have successfully reached the Mason VLAN 30 gateway through the physical network.


## Centralized DHCP Architecture

Kea DHCP runs on the Mason Ubuntu Server at `10.10.30.20`.

Troy uses DHCP relay to obtain centralized address configuration across the routed WAN. TROY-SW1 has DHCP relay configured on its VLAN interfaces, forwarding client requests to the Kea DHCP server at `10.10.30.20`.

DHCP address assignment has been validated for Troy VLAN 20 and VLAN 30. The VLAN 30 Legacy/OT DHCP test succeeded before deployment of the isolation ACLs; DHCP functionality after ACL deployment remains unverified.

`ip helper-address 10.10.30.20`

This allows DHCP traffic from the Troy employee network to reach the Kea server even though the server resides on the remote Mason server network.

TROY-WIN11-01 successfully received an address from the `10.20.20.0/24` scope along with:

- Default gateway `10.20.20.1`
- DNS server `10.10.30.10`
- DNS suffix `masonmfg.internal`

This architecture centralizes DHCP services at Mason while supporting remote Troy networks through Layer 3 DHCP relay.

---



## Security Edge and Internet Architecture

The FortiGate virtual firewall serves as the centralized security boundary between the enterprise network and external networks.

MASON-R1 connects the internal routed enterprise network to the FortiGate through the `10.10.40.0/30` transit network. MASON-R1 uses `10.10.40.1` as its next hop for the default route toward the FortiGate.

The FortiGate maintains routing toward the internal enterprise networks and provides firewall policy enforcement and NAT for Internet-bound traffic.

### FortiGate Security Policy Enforcement

The FortiGate provides centralized firewall policy enforcement for traffic crossing the enterprise security boundary.

- Configured firewall policies control permitted and denied traffic.
- Firewall policy counters and traffic logs provide visibility into traffic matching those policies.
- Controlled testing demonstrated permitted and denied traffic behavior.
- Before-and-after screenshots documented changes in firewall policy counters. Counter increases demonstrate traffic matching the policies, not necessarily a firewall configuration change.
- FortiGate firewall policy validation is documented separately from the unresolved Mason-to-FortiGate transit connectivity issue.

The FortiGate transit network (`10.10.40.0/30`) requires revalidation before current end-to-end Internet connectivity can be considered confirmed.

### Internet Traffic Path

Traffic from the Troy employee network follows the centralized path:

`TROY-WIN11-01 → TROY-SW1 → Mason-Troy WAN → MASON-R1 → FortiGate → External Network`

MASON-R1 advertises its default route through OSPF using:

`default-information originate`

TROY-SW1 therefore dynamically learns:

`O*E2 0.0.0.0/0 via 10.255.0.1`

This provides the Troy site with an Internet path without requiring a separate static default route on TROY-SW1.

End-to-end Internet connectivity has been validated from TROY-WIN11-01 using a successful ping to `8.8.8.8`.

The FortiGate remains the centralized policy enforcement point for traffic leaving the enterprise network.

The Troy Legacy/OT VLAN 30 network is protected by implemented extended ACLs on TROY-SW1. Controlled before-and-after testing confirmed that these ACLs restrict routed communication with other enterprise networks and external destinations.

FortiGate firewall policies provide additional security enforcement at the enterprise perimeter. The Legacy/OT ACL validation and FortiGate firewall policy validation are documented separately.

### FortiGate Transit Validation Status

The FortiGate Internet path was previously validated through successful external connectivity tests from Mason infrastructure and the Troy Windows 11 workstation.

During subsequent testing, connectivity across the dedicated `10.10.40.0/30` transit network failed.

- MASON-R1 transit address: `10.10.40.2/30`
- FortiGate port3 address: `10.10.40.1/30`
- Both interfaces appeared operational.
- MASON-R1 reported an incomplete ARP entry for `10.10.40.1`.
- Bidirectional transit connectivity failed.

The exact root cause has not been established, and restoration of this specific transit connection has not been independently validated.

The earlier successful Internet tests remain valid historical evidence, but current FortiGate transit connectivity requires revalidation.

Further investigation is documented in [Troubleshooting Case 13](troubleshooting.md).
