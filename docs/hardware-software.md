# Hardware and Software



This document identifies the physical hardware, virtual infrastructure, operating systems, and software used to build the Mason-Troy Enterprise Network.



## Physical Networking Hardware



| Device | Model | Location | Role |

|---|---|---|---|

| MASON-R1 | Cisco 2901 Integrated Services Router | Mason | Mason inter-VLAN routing, WAN routing, and connection toward the security edge |

| MASON-SW1 | Cisco Catalyst WS-C3560-24PS-S | Mason | Layer 2 access switching for Mason VLANs and physical/virtual infrastructure connectivity |

| TROY-SW1 | Cisco Catalyst WS-C3560-24PS-S | Troy | Layer 3 switching, Troy inter-VLAN routing, and OSPF WAN connectivity |

| Legacy Manufacturing System | Windows XP physical system | Troy | Legacy manufacturing/OT endpoint in VLAN 30; static IP configuration and extended ACL isolation validated |




### Cisco Switch Roles



The two Catalyst 3560 switches use different Cisco IOS feature sets. The switch assigned to Troy runs the Advanced IP Services image and supports the Layer 3 and OSPF functionality required at the manufacturing site. The Mason switch runs an IP Base image and is used as a Layer 2 access switch.



This design allows the available physical hardware to be used according to its capabilities without requiring an IOS upgrade.



## Virtualization and Host Infrastructure



### Primary Virtualization Host



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



### Secondary Host



The secondary virtualization host is a Windows 11 desktop computer used to support the Troy portion of the Mason-Troy Enterprise Network.

**Hardware specifications:**
- Processor: Intel Core i7-9700K
- Memory: 32 GB DDR4
- Operating system: Windows 11 Home
- Network connectivity: Wired Ethernet, Wi-Fi, and USB-to-Ethernet adapter

**Project responsibilities:**
- Hosts GNS3 and its virtual networking infrastructure.
- Supports the Troy Windows 11 virtual workstation.
- Provides physical connectivity between GNS3 and TROY-SW1.
- Supports endpoint testing, DHCP validation, and Legacy/OT VLAN 30 connectivity testing.
- Provides an additional virtualization environment for troubleshooting and network validation.



## Virtual Systems and Software



### Windows Server 2025


Windows Server 2025 Standard Evaluation provides the primary Microsoft enterprise services for the Mason network.


**Current roles:**

- Active Directory Domain Services (AD DS)
- DNS Server
- Domain Controller for `masonmfg.internal`
- Global Catalog
- Group Policy management for Mason and Troy workstations
- Windows Security auditing and Event Viewer logging
- SMB file sharing through `CompanyShare`
- Active Directory security group-based resource access control

**Validated functionality:**

- Domain authentication from Mason and Troy Windows 11 workstations
- Active Directory OU and security group organization
- Workstation Group Policy application
- Successful cross-site SMB file access and modification
- NTFS and SMB share permissions
- Windows Security auditing configured through a dedicated Group Policy Object (GPO).
- Advanced Audit Policy settings verified for authentication, Kerberos, user account management, security group management, computer account management, and directory service changes.
- Security Event IDs 4624, 4625, 4768, 4769, 4738, 4728, 4729, 4737, and 5136 observed during validation.
- Active Directory object-change auditing validated using an organizational unit (OU) System Access Control List (SACL) and Event ID 5136.
- Computer Account Management auditing confirmed through effective policy settings; corresponding event generation was not independently tested.
- Internal DNS and external domain resolution


**Network configuration:**

- IP address: `10.10.30.10/24`

- Default gateway: `10.10.30.1`

- Mason VLAN 30 — Servers



### Windows 11 Enterprise Workstations

Two Windows 11 Pro virtual machines provide employee endpoint testing at the Mason and Troy sites.

| Workstation | Site | VLAN | Operating System |
|---|---|---|---|
| MASON-WIN11-01 | Mason | 20 — Employees | Windows 11 Pro |
| TROY-WIN11-01 | Troy | 20 — Employees | Windows 11 Pro |

**Validated functionality:**

- Centralized Kea DHCP address assignment
- Active Directory domain membership
- Domain user authentication
- Group Policy application
- Cross-site connectivity and DNS resolution

The Troy workstation was additionally used to validate cross-site SMB file sharing with the Mason Windows Server.

Both workstations run as virtual machines within the GNS3 environment.



### Ubuntu Server



Ubuntu Server provides Linux-based infrastructure services and will support additional centralized network services as the project develops.




**Implemented services:**

- Kea DHCPv4 — centralized DHCP for all six Mason and Troy VLANs
- DHCP service administration through Ubuntu Server

**Planned services:**

- Centralized syslog collection
- NTP time synchronization
- Additional Linux-based monitoring services

**Administration:**

- SSH-based remote administration



**Network configuration:**

- IP address: `10.10.30.20/24`

- Default gateway: `10.10.30.1`

- Mason VLAN 30 — Servers



### FortiGate



A FortiGate virtual firewall provides the security edge between the enterprise network and the Internet.



**Platform:**

- FortiGate-VM64-KVM

- FortiOS 7.4.12

- Hosted within GNS3



**Implemented functionality:**

- Centralized Internet security edge for the Mason-Troy enterprise
- Internal-to-Internet firewall policy
- Network Address Translation (NAT)
- Static routing toward internal enterprise networks
- Previously validated Internet connectivity from Mason and Troy
- Firewall policy logging and traffic monitoring
- Validated permitted and denied traffic behavior
- Firewall policy hit counters and traffic logs used as security validation evidence

**Current validation status:**

The FortiGate Internet path was previously operational. A subsequent ARP failure on the `10.10.40.0/30` transit network remains unresolved and requires revalidation.

**Planned enhancements:**

- Basic firewall management hardening
- Additional security validation




### GNS3



GNS3 provides the virtual networking environment used to integrate virtual servers and security appliances with the physical Cisco infrastructure.



The environment includes:

- Virtual Ethernet switching

- GNS3 Cloud interfaces for physical network bridging

- FortiGate virtualization

- Windows Server virtualization

- Ubuntu Server virtualization

- GNS3 NAT for upstream Internet connectivity



## Supporting Tools



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
