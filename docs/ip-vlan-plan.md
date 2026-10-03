\# IP Addressing and VLAN Plan



This document defines the VLAN and IPv4 addressing scheme used throughout the Mason-Troy Enterprise Network.



\## Mason — Corporate Headquarters



| VLAN | Name | Subnet | Default Gateway | Purpose |

|---|---|---|---|---|

| 10 | Management | 10.10.10.0/24 | 10.10.10.1 | Network device management |

| 20 | Employees | 10.10.20.0/24 | 10.10.20.1 | Employee and business endpoints |

| 30 | Servers | 10.10.30.0/24 | 10.10.30.1 | Server infrastructure |

| 999 | Native | N/A | N/A | Dedicated unused native VLAN |



\### Infrastructure Addresses



| Device | Interface / Role | IP Address |

|---|---|---|

| MASON-R1 | VLAN 10 Gateway | 10.10.10.1 |

| MASON-R1 | VLAN 20 Gateway | 10.10.20.1 |

| MASON-R1 | VLAN 30 Gateway | 10.10.30.1 |

| MASON-SW1 | Management SVI | 10.10.10.2 |

| Windows Server 2025 | Server | 10.10.30.10 |

| Ubuntu Server | Server | 10.10.30.20 |



\## Troy — Manufacturing Facility



| VLAN | Name | Subnet | Default Gateway | Purpose |

|---|---|---|---|---|

| 10 | Management | 10.20.10.0/24 | 10.20.10.1 | Network device management |

| 20 | Employees | 10.20.20.0/24 | 10.20.20.1 | Employee and business endpoints |

| 30 | Legacy-OT | 10.20.30.0/24 | 10.20.30.1 | Isolated legacy manufacturing and OT systems |

| 999 | Native | N/A | N/A | Reserved native VLAN |



\### Infrastructure Addresses



| Device | Interface / Role | IP Address |

|---|---|---|

| TROY-SW1 | VLAN 10 Gateway | 10.20.10.1 |

| TROY-SW1 | VLAN 20 Gateway | 10.20.20.1 |

| TROY-SW1 | VLAN 30 Gateway | 10.20.30.1 |

| Legacy Windows XP System | Manufacturing / OT Endpoint | 10.20.30.10 (Planned) |



\## Mason–Troy WAN



The Mason and Troy sites are connected using a point-to-point routed link.



| Device | Interface / Role | IP Address |

|---|---|---|

| MASON-R1 | Troy WAN | 10.255.0.1/30 |

| TROY-SW1 | Mason WAN | 10.255.0.2/30 |



\*\*WAN Network:\*\* `10.255.0.0/30`



OSPF Area 0 is used across this link to dynamically exchange the Mason and Troy networks.



\## Addressing Design



The addressing scheme was designed to make each site and network function easy to identify.



\- Mason networks use the `10.10.x.0/24` address space.

\- Troy networks use the `10.20.x.0/24` address space.

\- Matching VLAN IDs are used at both sites where possible to maintain consistency.

\- VLAN 10 is reserved for management traffic.

\- VLAN 20 is used for normal employee and business traffic.

\- VLAN 30 is assigned according to each site's infrastructure requirements: servers at Mason and legacy/OT manufacturing systems at Troy.

\- VLAN 999 is reserved as the native VLAN and is not intended for endpoint traffic.

\- The `10.255.0.0/30` network is dedicated to the point-to-point WAN connection between Mason and Troy.





