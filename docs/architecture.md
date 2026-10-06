\# Network Architecture



This document describes the physical and virtual architecture of the Mason-Troy Enterprise Network and how the two locations communicate.



\## Overall Design



The project represents a two-site enterprise and manufacturing environment consisting of:



\- \*\*Mason, Ohio — Corporate Headquarters\*\*

\- \*\*Troy, Ohio — Manufacturing Facility\*\*



The sites are connected through a routed point-to-point WAN. OSPF Area 0 provides dynamic route exchange between the locations.



Mason uses router-on-a-stick inter-VLAN routing through MASON-R1, while Troy uses Layer 3 switching on TROY-SW1. This design demonstrates two different methods of providing inter-VLAN routing within the same enterprise environment.



\## Mason Architecture



Mason serves as the corporate headquarters and hosts the project's primary server and network service infrastructure.



\### Network Components



\- \*\*MASON-R1 — Cisco 2901\*\*

&#x20; - Provides router-on-a-stick inter-VLAN routing.

&#x20; - Acts as the Mason endpoint of the routed WAN.

&#x20; - Advertises Mason networks into OSPF.

&#x20; - Provides the upstream path toward the FortiGate security edge and Internet.



\- \*\*MASON-SW1 — Cisco Catalyst 3560\*\*

&#x20; - Operates as a Layer 2 access switch.

&#x20; - Provides VLAN connectivity for management, employee, and server networks.

&#x20; - Uses an 802.1Q trunk to MASON-R1.

&#x20; - Uses an additional 802.1Q trunk to connect physical VLANs with the GNS3 virtual environment.



\- \*\*Windows Server 2025\*\*

&#x20; - Located in Mason VLAN 30.

&#x20; - Provides Active Directory Domain Services and DNS.



\- \*\*Ubuntu Server\*\*

&#x20; - Located in Mason VLAN 30.

&#x20; - Provides centralized Kea DHCP and other Linux-based infrastructure services.



\### Mason VLANs



\- VLAN 10 — Management

\- VLAN 20 — Employees

\- VLAN 30 — Servers

\- VLAN 999 — Native VLAN



\## Troy Architecture



Troy represents the manufacturing facility and contains both standard business systems and the legacy manufacturing environment.



\### Network Components



\- \*\*TROY-SW1 — Cisco Catalyst 3560\*\*

&#x20; - Operates as a Layer 3 switch.

&#x20; - Provides the default gateways for Troy VLANs using switched virtual interfaces (SVIs).

&#x20; - Performs inter-VLAN routing.

&#x20; - Acts as the Troy endpoint of the routed WAN.

&#x20; - Participates directly in OSPF Area 0 with MASON-R1.



\- \*\*Employee Systems\*\*

&#x20; - Located in VLAN 20.

&#x20; - Provide normal business connectivity at the manufacturing facility.

&#x20; - TROY-WIN11-01 provides the current Windows 11 enterprise client used for DHCP, Active Directory, Group Policy, DNS, and routed connectivity validation.

&#x20; - TROY-WIN11-01 receives centralized DHCP service from the Mason Ubuntu Server through DHCP relay on TROY-SW1.





\- \*\*Legacy Windows XP Manufacturing System\*\*

&#x20; - Located in VLAN 30 — Legacy/OT.

&#x20; - Represents an older system that remains necessary for manufacturing operations.

&#x20; - Will be isolated from unnecessary enterprise and Internet access using VLAN segmentation, extended ACLs, and firewall policies.

&#x20; - Only explicitly required communication will be permitted once the security policy is implemented.



\### Troy VLANs



\- VLAN 10 — Management

\- VLAN 20 — Employees

\- VLAN 30 — Legacy/OT

\- VLAN 999 — Native VLAN



\## WAN and Dynamic Routing



Mason and Troy are connected using a routed point-to-point WAN network.



\### WAN Addressing



\- Network: `10.255.0.0/30`

\- MASON-R1: `10.255.0.1`

\- TROY-SW1: `10.255.0.2`



\### OSPF



OSPF process 1 and Area 0 are used to dynamically exchange routes between the two sites.

MASON-R1 also advertises its default route into OSPF. TROY-SW1 learns `0.0.0.0/0` through MASON-R1 at `10.255.0.1`, providing Troy with a dynamically learned path toward the centralized FortiGate Internet edge.



MASON-R1 advertises:



\- `10.10.10.0/24` — Mason Management

\- `10.10.20.0/24` — Mason Employees

\- `10.10.30.0/24` — Mason Servers

\- `10.255.0.0/30` — WAN



TROY-SW1 advertises:



\- `10.20.10.0/24` — Troy Management

\- `10.20.20.0/24` — Troy Employees

\- `10.20.30.0/24` — Troy Legacy/OT

\- `10.255.0.0/30` — WAN



A full OSPF adjacency has been established between MASON-R1 and TROY-SW1. Bidirectional route propagation has been validated, allowing both sites to dynamically learn the remote site's networks.



\## Physical and Virtual Network Integration



The project combines physical Cisco infrastructure with virtual systems hosted in GNS3.



At Mason, virtual servers connect to a GNS3 Ethernet switch configured with access ports for the appropriate VLANs. The virtual switch uses an 802.1Q trunk to a GNS3 Cloud interface, which bridges the virtual network to a physical USB-to-Ethernet adapter on the virtualization host.



The USB-to-Ethernet adapter connects to MASON-SW1 Fa0/5, which is configured as an 802.1Q trunk carrying VLANs 10, 20, 30, and 999.



\### Virtual-to-Physical Traffic Path



For a virtual server in Mason VLAN 30, the traffic path is:



`Virtual Server → GNS3 Ethernet Switch → GNS3 Cloud → USB-to-Ethernet Adapter → MASON-SW1 → MASON-R1`



This design allows virtual systems to participate directly in the same VLAN and routing infrastructure as the physical Cisco equipment.



\### Current Virtual Switch Layout



\- Ports 2–3 — Access VLAN 10

\- Ports 5–7 — Access VLAN 20

\- Ports 9–11 — Access VLAN 30

\- Port 12 — 802.1Q trunk toward the physical Mason network



Windows Server 2025 currently connects through port 9, and Ubuntu Server connects through port 10. Both systems have successfully reached the Mason VLAN 30 gateway through the physical network.


## Centralized DHCP Architecture

Kea DHCP runs on the Mason Ubuntu Server at `10.10.30.20`.

Troy uses DHCP relay to obtain centralized address configuration across the routed WAN. TROY-SW1 VLAN 20 is configured with:

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

The legacy Windows XP manufacturing environment at Troy will not receive normal unrestricted Internet access. Planned extended ACL and firewall controls will enforce least-privilege isolation for the Legacy/OT VLAN.
