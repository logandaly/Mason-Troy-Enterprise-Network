# Mason–Troy Enterprise Network

## Overview

The Mason–Troy Enterprise Network is a **two-site hybrid enterprise/manufacturing network** integrating physical Cisco routing and switching equipment with virtualized infrastructure in GNS3. It provides segmented business connectivity between Mason (corporate headquarters) and Troy (manufacturing), centralized enterprise services, and controlled Internet access through a FortiGate virtual firewall.

The project demonstrates hands-on network design, systems administration, security, troubleshooting, and Python automation. **A physical Windows XP manufacturing endpoint was deployed and tested on Troy's Legacy/OT VLAN 30, with extended ACLs implemented and validated to restrict unauthorized routed communication.**

**Project evidence:** [Network validation](docs/validation.md) · [Troubleshooting](docs/troubleshooting.md) · [IP/VLAN plan](docs/ip-vlan-plan.md) · [Python monitoring](automation/network-monitoring/README.md)

## Project Highlights

- **Hybrid lab:** Physical Cisco router and Catalyst switches integrated with GNS3-hosted Windows Server, Ubuntu Server, Windows clients, and a FortiGate VM.
- **Two-site routing:** OSPF Area 0 adjacency and route exchange across `10.255.0.0/30`, with a default route propagated toward Troy.
- **Six principal VLANs:** Management, employee, and server/Legacy-OT networks at the two sites, with a separate Mason firewall-transit network.
- **Enterprise services:** Windows Server 2025 Active Directory Domain Services, DNS, Group Policy, auditing, SMB file sharing, and centralized Ubuntu Kea DHCP with Cisco relay.
- **Security:** FortiGate policy controls and NAT, bidirectional extended ACL isolation for Troy Legacy/OT VLAN 30, Cisco switch/management hardening, and group-based SMB/NTFS permissions.
- **Verified results:** Successful cross-site ping and three-hop traceroutes in both directions; Mason server TCP/443 reachability and Troy workstation HTTPS response (`HTTP/1.1 200 OK`).
- **Automation:** Python/Netmiko monitoring successfully collected **30 of 30 planned commands** from MASON-R1, MASON-SW1, and TROY-SW1.

## Key Technologies

Cisco IOS routing and switching · VLANs and 802.1Q trunks · OSPF · Extended ACLs · FortiGate VM and NAT · Windows Server 2025 · Active Directory and Group Policy · DNS · Ubuntu and Kea DHCP · DHCP relay · GNS3 · Windows 11 · Python and Netmiko · PowerShell · Git and GitHub

## Network Architecture

The network represents two locations in Ohio:

- **Mason — Corporate Headquarters:** Physical MASON-R1 and MASON-SW1; primary Windows Server 2025 and Ubuntu infrastructure; centralized network services and FortiGate Internet edge.
- **Troy — Manufacturing Facility:** Physical TROY-SW1 Layer 3 switch; employee workstation connectivity; and the segregated Legacy/OT VLAN 30.

The sites are linked by the point-to-point **`10.255.0.0/30`** WAN (MASON-R1 `10.255.0.1`, TROY-SW1 `10.255.0.2`). OSPF exchanges the site networks. At Mason, MASON-R1 uses router-on-a-stick subinterfaces for VLAN routing, while TROY-SW1 provides Layer 3 switching at Troy. The FortiGate is a **virtual appliance**, connected via Mason's firewall transit network (`10.10.40.0/30`) and an upstream simulated/lab Internet path.

| Site | VLAN | Purpose | Subnet |
|---|---:|---|---|
| Mason | 10 | Management | `10.10.10.0/24` |
| Mason | 20 | Employees | `10.10.20.0/24` |
| Mason | 30 | Servers | `10.10.30.0/24` |
| Troy | 10 | Management | `10.20.10.0/24` |
| Troy | 20 | Employees | `10.20.20.0/24` |
| Troy | 30 | Legacy / OT | `10.20.30.0/24` |

Mason additionally uses VLAN 40 for firewall transit and VLAN 999 as a native/management VLAN in the trunk design. See the [complete IP addressing and VLAN plan](docs/ip-vlan-plan.md) for device-specific addressing and DHCP scopes.

## Project Goals and Outcomes

| Goal | Documented outcome |
|---|---|
| Connect physical and virtual infrastructure | Implemented and validated |
| Segment sites and traffic classes | Implemented VLAN segmentation and routing |
| Establish intersite routing | OSPF neighbor FULL; bidirectional route propagation verified |
| Centralize identity, DNS, and DHCP | AD DS/DNS deployed; six-VLAN Kea DHCP and relay validated |
| Apply layered security | FortiGate policies, Troy Legacy/OT ACLs, SSH/port hardening, and SMB/NTFS DAC tested to the extent described in validation records |
| Demonstrate external connectivity | Mason TCP/443 and Troy HTTPS tests passed |
| Automate monitoring | Netmiko read-only collection: 30/30 planned commands |
| Document and troubleshoot | Repository records tests, limitations, screenshots, and troubleshooting investigations |

## Current Project Status

### Completed and Validated

- Physical Mason and Troy Cisco networking infrastructure and GNS3 integration.
- VLAN segmentation, Mason router-on-a-stick routing, and Troy Layer 3 SVIs.
- Point-to-point Mason–Troy WAN, OSPF FULL adjacency, bidirectional routes, and OSPF default-route propagation.
- Windows Server 2025 and Ubuntu Server deployments, AD DS forest `masonmfg.internal`, AD DNS and reverse DNS.
- Mason and Troy OUs, user accounts, security groups, domain-joined Windows workstations, and tested workstation GPOs.
- Centralized Kea DHCP scopes for all six principal VLANs, with associated client validation and remote DHCP relay.
- Windows auditing and observed successful security events; cross-site SMB/CompanyShare access and file modification using group-based permissions.
- Troy Legacy/OT VLAN 30 routed isolation with bidirectional ACLs and deny-counter evidence.
- FortiGate firewall policy configuration, NAT, traffic logging, and successful external application connectivity from both sites.
- Cisco management hardening (including SSHv2), selected switch port security, PortFast, and BPDU Guard configuration verification.
- Resolved GNS3/USB Ethernet port-security issue affecting the Troy workstation; subsequent DHCP and cross-site connectivity restored.
- Bidirectional Mason–Troy three-hop traceroutes and four final routing/Internet-validation screenshots.
- Read-only Python/Netmiko monitoring with **30/30** commands successfully collected from three physical Cisco devices.
- Wireless client-volume, bandwidth, AP placement, and security **assessment** for a possible future deployment (not a deployed WLAN).

### Remaining Limitations and Optional Future Work

- FortiGate VMnet1 management connectivity investigation and further management hardening.
- Confirm why Internet-directed ICMP ping/traceroute was inconsistent in later tests; FortiGate service restrictions are a leading explanation, **not a log-confirmed root cause**. HTTPS connectivity was validated separately.
- Mason-specific user Group Policy behavior remains partially untested.
- Investigate the historical direct-UNC-navigation restriction for CompanyShare (mapped drive read/write was validated).
- Revalidate DHCP on Troy Legacy/OT VLAN 30 after ACL enforcement.
- Optional unauthorized-device port-security and BPDU Guard behavior tests, and independent Telnet-rejection validation.
- Further Wireshark packet analysis, centralized monitoring/logging, and automated configuration backups.
- Wireless deployment, RF survey, and throughput testing remain **future work**, not completed features. The physical Windows XP Legacy/OT endpoint was tested as part of the completed project.

The [validation document](docs/validation.md) distinguishes completed behavior tests from configuration-only verification and outstanding work. A successful HTTPS test does not by itself establish that every Internet protocol is permitted.

## Project Documentation and Evidence

| Document | Contents |
|---|---|
| [Network Architecture](docs/architecture.md) | Physical/virtual topology, intersite routing, and enterprise services |
| [IP Addressing and VLAN Plan](docs/ip-vlan-plan.md) | Subnets, VLANs, gateways, and DHCP scope design |
| [Hardware and Software Inventory](docs/hardware-software.md) | Physical Cisco devices, virtual systems, and supporting tools |
| [Project Milestones](docs/milestones.md) | Implementation progress and significant checkpoints |
| [Network Validation](docs/validation.md) | Tests and linked screenshots for routing, DHCP, AD, firewall, ACLs, and connectivity |
| [Troubleshooting Cases](docs/troubleshooting.md) | Symptoms, diagnostic steps, confirmed findings, fixes, and limitations |
| [Wireless Assessment](docs/wireless-assessment.md) | Proposed client volume, bandwidth, placement, security, and validation plan |
| [Python Network Monitoring](automation/network-monitoring/README.md) | Netmiko monitoring workflow, configuration, and validation results |

### Selected Final Validation Evidence

- [Troy Windows 11 → Mason Windows Server traceroute](screenshots/routing/Troy-Win11-to-Mason-Server-Traceroute-Validation.png)
- [Mason Windows Server → Troy Windows 11 traceroute](screenshots/routing/Mason-Server-to-Troy-VLAN20-Traceroute-Validation.png)
- [Mason Windows Server external TCP/443 test](screenshots/routing/Mason-WindowsServer-VLAN30-HTTPS-Internet-Validation.png)
- [Troy Windows 11 external HTTPS response](screenshots/routing/Troy-Win11-VLAN20-HTTPS-Internet-Validation.png)
- [Cisco OSPF routing and management hardening evidence](screenshots/routing/Mason-R1-OSPF-Hardening-and-Adjacency-Validation.png)

## Repository Structure

- `automation/network-monitoring/` — Python/Netmiko network monitoring code and instructions.
- `docs/` — Architecture, VLAN plan, inventory, milestones, validation, troubleshooting, and wireless assessment.
- `screenshots/` — Captured implementation, security, routing, and connectivity evidence.

Additional configuration examples and diagrams, where present, supplement the linked documentation. The GitHub documents and screenshots are the primary evidence index for this portfolio.

## Validation Approach

**Build → Verify Configuration → Test → Troubleshoot → Retest → Document → Commit**

A configuration is not described as behaviorally validated unless supporting testing was actually performed. Sensitive credentials are excluded from published evidence.
