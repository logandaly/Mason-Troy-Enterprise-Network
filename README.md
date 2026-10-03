\# Mason-Troy Enterprise Network



\## Overview



This project is a segmented two-site enterprise and manufacturing network designed to allow normal business traffic to communicate between locations and access the Internet while securely isolating a legacy Windows XP system required for manufacturing operations.



The purpose of this project is to demonstrate the networking, systems administration, security, and troubleshooting skills I developed throughout my education by designing and implementing a small enterprise network using both physical and virtual infrastructure.





\## Key Technologies



\- Cisco routing and switching

\- VLAN segmentation

\- Inter-VLAN routing

\- OSPF dynamic routing

\- Extended access control lists (ACLs)

\- FortiGate firewall

\- Windows Server 2025

\- Active Directory Domain Services (AD DS)

\- DNS

\- Ubuntu Server

\- DHCP and DHCP relay

\- GNS3 virtualization

\- Python and Netmiko automation

\- Wireshark network analysis and validation





\## Network Architecture



The network represents two business locations in Ohio:



\- \*\*Mason — Corporate Headquarters:\*\* Hosts the primary server infrastructure, network services, security edge, and centralized management resources.

\- \*\*Troy — Manufacturing Facility:\*\* Provides connectivity for standard business systems while maintaining a segmented legacy/OT environment for manufacturing equipment.



The two sites are connected through a routed WAN and use OSPF for dynamic route exchange. VLANs separate network functions and device types, while routing, ACLs, and firewall policies provide controlled communication between network segments.



The environment combines physical Cisco networking equipment with virtualized infrastructure in GNS3, allowing the project to incorporate real hardware while using virtualization for servers, security appliances, and other systems where appropriate.





\## Project Goals



\- Design and implement a functional two-site enterprise network using physical and virtual infrastructure.

\- Segment business, management, server, and manufacturing traffic using VLANs.

\- Provide dynamic routing between the Mason and Troy sites using OSPF.

\- Deploy centralized network services including Active Directory, DNS, and DHCP.

\- Provide controlled Internet connectivity through a FortiGate security firewall.

\- Securely isolate the legacy Windows XP manufacturing environment using VLAN segmentation, ACLs, and firewall policies.

\- Apply network and switch hardening techniques to reduce unnecessary access and services.

\- Automate basic network administration and configuration backup tasks using Python and Netmiko.

\- Validate network functionality and troubleshoot problems using Cisco IOS commands, server administration tools, and Wireshark.

\- Document the design, implementation, troubleshooting process, and validation results as a technical portfolio project.





\## Current Project Status



\### Completed



\- Physical Mason and Troy Cisco network infrastructure

\- VLAN creation and initial network segmentation

\- Mason router-on-a-stick inter-VLAN routing

\- Troy Layer 3 switching and inter-VLAN routing

\- Routed WAN connection between Mason and Troy

\- OSPF adjacency and bidirectional route propagation between sites

\- GNS3 integration with the physical Mason network

\- Windows Server 2025 deployment

\- Ubuntu Server deployment

\- Active Directory Domain Services deployment

\- `masonmfg.internal` Active Directory forest and domain

\- AD-integrated DNS configuration

\- Forward and reverse DNS configuration and validation

\- Bidirectional communication between Windows and Ubuntu servers



\### In Progress / Planned



\- Active Directory organizational structure and domain clients

\- DHCP services using Ubuntu Server

\- DHCP relay across network segments

\- FortiGate integration and Internet connectivity

\- Legacy Windows XP / manufacturing network isolation

\- ACL and firewall security policies

\- Network device hardening

\- Centralized logging and monitoring

\- Python/Netmiko network automation

\- Wireshark validation and troubleshooting

\- End-to-end security and connectivity testing



\## Repository Structure



\- `automation/` — Python and Netmiko network automation scripts

\- `configs/` — Sanitized device configuration backups

&#x20; - `mason/` — Mason router and switch configurations

&#x20; - `troy/` — Troy switch configurations

&#x20; - `fortigate/` — FortiGate configuration documentation

\- `diagrams/` — Network topology and architecture diagrams

\- `docs/` — Detailed project documentation

&#x20; - `architecture.md` — Physical and virtual network architecture

&#x20; - `hardware-software.md` — Hardware, operating systems, and software used

&#x20; - `ip-vlan-plan.md` — VLAN, subnet, gateway, and addressing plan

&#x20; - `milestones.md` — Project implementation progress

&#x20; - `troubleshooting.md` — Problems encountered, investigation, fixes, and lessons learned

&#x20; - `validation.md` — Connectivity, routing, service, and security validation

\- `screenshots/` — Supporting configuration and validation evidence





