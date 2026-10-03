\# Hardware and Software



This document identifies the physical hardware, virtual infrastructure, operating systems, and software used to build the Mason-Troy Enterprise Network.



\## Physical Networking Hardware



| Device | Model | Location | Role |

|---|---|---|---|

| MASON-R1 | Cisco 2901 Integrated Services Router | Mason | Mason inter-VLAN routing, WAN routing, and connection toward the security edge |

| MASON-SW1 | Cisco Catalyst WS-C3560-24PS-S | Mason | Layer 2 access switching for Mason VLANs and physical/virtual infrastructure connectivity |

| TROY-SW1 | Cisco Catalyst WS-C3560-24PS-S | Troy | Layer 3 switching, Troy inter-VLAN routing, and OSPF WAN connectivity |

| Legacy Manufacturing System | Windows XP physical system | Troy | Legacy manufacturing/OT endpoint requiring network isolation |



\### Cisco Switch Roles



The two Catalyst 3560 switches use different Cisco IOS feature sets. The switch assigned to Troy runs the Advanced IP Services image and supports the Layer 3 and OSPF functionality required at the manufacturing site. The Mason switch runs an IP Base image and is used as a Layer 2 access switch.



This design allows the available physical hardware to be used according to its capabilities without requiring an IOS upgrade.



\## Virtualization and Host Infrastructure



\### Primary Virtualization Host



The primary virtualization host is an ASUS ROG Strix G512LW laptop used to run GNS3 and the virtual infrastructure required by the project.



| Component | Specification |

|---|---|

| CPU | Intel Core i7-10750H, 6 cores / 12 threads |

| Memory | 32 GB DDR4 |

| Storage | 500 GB Samsung SSD + 1 TB WD PC SN530 |

| GPU | NVIDIA GeForce RTX 2070 |

| Primary Virtualization Platform | GNS3 |

| Internet Connection | Wi-Fi |

| Physical Lab Connectivity | Built-in Gigabit Ethernet and USB-to-Ethernet adapter |



The laptop provides the bridge between the virtual GNS3 environment and the physical Cisco network. Wi-Fi provides upstream Internet connectivity, while separate Ethernet interfaces are used to connect virtual infrastructure to the physical lab.



\### Secondary Host



A desktop computer is available at the Troy site for endpoint and virtualization duties as required. The system contains 32 GB of RAM and provides both wired Ethernet and Wi-Fi connectivity.



\## Virtual Systems and Software



\### Windows Server 2025



Windows Server 2025 Standard Evaluation provides the primary Microsoft enterprise services for the Mason network.



\*\*Current roles:\*\*

\- Active Directory Domain Services (AD DS)

\- DNS Server

\- Domain Controller for `masonmfg.internal`

\- Global Catalog



\*\*Network configuration:\*\*

\- IP address: `10.10.30.10/24`

\- Default gateway: `10.10.30.1`

\- Mason VLAN 30 — Servers



\### Ubuntu Server



Ubuntu Server provides Linux-based infrastructure services and will support additional centralized network services as the project develops.



\*\*Current and planned roles:\*\*

\- Kea DHCP

\- Centralized syslog collection

\- NTP

\- SSH administration



\*\*Network configuration:\*\*

\- IP address: `10.10.30.20/24`

\- Default gateway: `10.10.30.1`

\- Mason VLAN 30 — Servers



\### FortiGate



A FortiGate virtual firewall provides the security edge between the enterprise network and the Internet.



\*\*Platform:\*\*

\- FortiGate-VM64-KVM

\- FortiOS 7.4.12

\- Hosted within GNS3



\*\*Planned responsibilities:\*\*

\- Internet edge security

\- Firewall policy enforcement

\- Controlled outbound Internet access

\- Additional protection between trusted enterprise networks and external networks



\### GNS3



GNS3 provides the virtual networking environment used to integrate virtual servers and security appliances with the physical Cisco infrastructure.



The environment includes:

\- Virtual Ethernet switching

\- GNS3 Cloud interfaces for physical network bridging

\- FortiGate virtualization

\- Windows Server virtualization

\- Ubuntu Server virtualization

\- GNS3 NAT for upstream Internet connectivity



\## Supporting Tools



| Tool | Purpose |

|---|---|

| Wireshark | Packet capture, protocol analysis, troubleshooting, and validation |

| Python | Network automation and scripting |

| Netmiko | SSH-based automation of Cisco network devices |

| Git | Local version control for project documentation and automation |

| GitHub | Public project repository and portfolio documentation |

| Npcap | Packet capture support for GNS3 and Windows networking |

| USB-to-Console Cable | Direct console administration of physical Cisco equipment |

| USB-to-Ethernet Adapter | Physical bridge between GNS3 virtual networks and the Cisco lab |

| PowerShell | Windows administration, network configuration, and troubleshooting |

