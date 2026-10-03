\# Project Milestones



This document tracks the implementation progress of the Mason-Troy Enterprise Network. Milestones are documented as the network is built, tested, and validated.



\## Milestone 1 — Physical Network and VLAN Foundation



\### Completed



\- Assigned physical Cisco equipment to the Mason and Troy sites.

\- Established Mason and Troy VLAN structures.

\- Configured management, employee, server, and legacy/OT network segments.

\- Configured VLAN 999 as a dedicated native VLAN.

\- Configured Mason router-on-a-stick inter-VLAN routing.

\- Configured Troy Layer 3 switching using SVIs.

\- Validated local VLAN gateway connectivity.



\### Design Decision



The two available Catalyst 3560 switches contained different IOS feature sets. The switch running Advanced IP Services was assigned to Troy because it supports the Layer 3 and OSPF functionality required by the design. The IP Base switch was assigned to Mason as a Layer 2 access switch.



This avoided an unnecessary IOS upgrade while making effective use of the available physical hardware.



\---



\## Milestone 2 — Mason-Troy WAN and OSPF



\### Completed



\- Converted TROY-SW1 Fa0/24 into a routed port.

\- Configured the `10.255.0.0/30` point-to-point WAN.

\- Assigned `10.255.0.1` to MASON-R1.

\- Assigned `10.255.0.2` to TROY-SW1.

\- Configured OSPF process 1 and Area 0.

\- Established a full OSPF adjacency between Mason and Troy.

\- Advertised the Mason and Troy VLAN networks through OSPF.

\- Verified bidirectional dynamic route propagation.

\- Saved validated Cisco configurations.



\### Validation



MASON-R1 successfully learned the Troy networks through `10.255.0.2`, while TROY-SW1 successfully learned the Mason networks through `10.255.0.1`.



\---



\## Milestone 3 — Physical and Virtual Network Integration



\### Completed



\- Integrated the GNS3 virtual environment with the physical Mason network.

\- Configured a GNS3 Ethernet switch with VLAN-aware access ports.

\- Configured GNS3 switch port 12 as an 802.1Q trunk.

\- Connected the trunk through a GNS3 Cloud interface to the host USB-to-Ethernet adapter.

\- Converted MASON-SW1 Fa0/5 into an 802.1Q trunk.

\- Allowed VLANs 10, 20, 30, and 999 across the physical/virtual trunk.

\- Verified trunk operation and Spanning Tree forwarding state.

\- Connected Windows Server and Ubuntu Server to Mason VLAN 30.

\- Verified virtual server connectivity through the physical Cisco infrastructure.



\### Troubleshooting



Initial virtual-to-physical connectivity failed because the host USB-to-Ethernet adapter still contained an old static Troy address of `10.20.30.10`.



The stale address was removed, allowing the adapter to operate strictly as part of the Layer 2 bridge. After the change, the virtual Windows Server successfully reached the Mason VLAN 30 gateway at `10.10.30.1`.



This validated the complete path between the GNS3 virtual environment and the physical Mason network.



\---



\## Milestone 4 — Server Infrastructure



\### Completed



\- Deployed Windows Server 2025 in the GNS3 environment.

\- Configured Windows Server with static address `10.10.30.10/24`.

\- Configured default gateway `10.10.30.1`.

\- Deployed Ubuntu Server in the GNS3 environment.

\- Configured Ubuntu Server with static address `10.10.30.20/24`.

\- Configured default gateway `10.10.30.1`.

\- Connected both servers to Mason VLAN 30.

\- Verified both servers could reach the Mason VLAN 30 gateway.

\- Verified bidirectional communication between Windows Server and Ubuntu Server.



\### Troubleshooting



Initial testing showed that Windows Server could successfully ping Ubuntu Server, but Ubuntu Server could not successfully ping Windows Server.



Network routing and VLAN connectivity were functioning correctly. Investigation identified Windows Firewall as the source of the asymmetric connectivity.



The built-in File and Printer Sharing firewall rule group was enabled to permit the required inbound ICMP traffic while leaving Windows Firewall enabled.



After the change, Ubuntu Server successfully reached Windows Server, confirming bidirectional server communication.



\---



\## Milestone 5 — Active Directory and DNS



\### Completed



\- Installed Active Directory Domain Services (AD DS) on Windows Server 2025.

\- Installed the Windows DNS Server role.

\- Promoted the server as the first domain controller in a new Active Directory forest.

\- Created the `masonmfg.internal` domain.

\- Configured the `MASONMFG` NetBIOS domain name.

\- Enabled DNS Server and Global Catalog functionality on the domain controller.

\- Verified the Active Directory-integrated DNS zones.

\- Verified automatically generated Kerberos, LDAP, kpasswd, and Global Catalog SRV records.

\- Created an IPv4 reverse lookup zone for the Mason server network.

\- Configured the reverse lookup zone to use secure dynamic updates.

\- Created and validated a PTR record for the domain controller at `10.10.30.10`.

\- Successfully validated reverse DNS resolution using `nslookup`.



\### Validation



The Active Directory domain and DNS infrastructure are operational. Forward DNS zones, Active Directory service records, and reverse DNS functionality have been verified.



This provides the foundation for future domain-joined clients, centralized authentication, DHCP integration, and additional enterprise services.





