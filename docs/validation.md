\# Network Validation



This document records the tests used to verify connectivity, routing, server communication, and enterprise services throughout the Mason-Troy Enterprise Network.



Validation is performed throughout the build process rather than only after the network is complete. Additional security, DHCP, Internet, automation, and legacy/OT validation will be added as those phases are implemented.



\## 1. Mason-Troy WAN Connectivity



\### Objective



Verify Layer 3 connectivity across the point-to-point WAN between Mason and Troy.



\### Network



\- MASON-R1: `10.255.0.1/30`

\- TROY-SW1: `10.255.0.2/30`

\- WAN Network: `10.255.0.0/30`



\### Result



Bidirectional connectivity across the WAN was successfully verified.



\*\*Status: PASS\*\*



\---



\## 2. OSPF Neighbor Adjacency



\### Objective



Verify that MASON-R1 and TROY-SW1 successfully establish an OSPF neighbor relationship.



\### Configuration



\- OSPF Process: 1

\- Area: 0

\- MASON-R1 Router ID: `10.255.0.1`

\- TROY-SW1 Router ID: `10.255.0.2`



\### Result



A full OSPF adjacency was successfully established between MASON-R1 and TROY-SW1.



\*\*Status: PASS\*\*



\---



\## 3. OSPF Route Propagation



\### Objective



Verify that both sites dynamically learn the remote site's networks.



\### Mason Learning Troy



MASON-R1 successfully learned:



\- `10.20.10.0/24`

\- `10.20.20.0/24`

\- `10.20.30.0/24`



Routes were learned through TROY-SW1 at `10.255.0.2`.



\### Troy Learning Mason



TROY-SW1 successfully learned:



\- `10.10.10.0/24`

\- `10.10.20.0/24`

\- `10.10.30.0/24`



Routes were learned through MASON-R1 at `10.255.0.1`.



\### Result



Bidirectional OSPF route propagation was successfully verified.



\*\*Status: PASS\*\*



\---



\## 4. Mason Physical/Virtual Trunk



\### Objective



Verify that the physical Mason network can carry VLAN traffic between GNS3 and MASON-SW1.



\### Configuration



MASON-SW1 Fa0/5 is configured as an 802.1Q trunk carrying:



\- VLAN 10

\- VLAN 20

\- VLAN 30

\- VLAN 999



VLAN 999 is configured as the native VLAN.



The trunk connects:



`GNS3 Switch → GNS3 Cloud → USB-to-Ethernet Adapter → MASON-SW1 Fa0/5`



\### Result



The trunk entered the forwarding state and successfully transported VLAN 30 traffic between virtual servers and the physical Cisco infrastructure.



\*\*Status: PASS\*\*



\---



\## 5. Windows Server Gateway Connectivity



\### Objective



Verify that Windows Server 2025 can communicate through the physical/virtual network bridge with its default gateway.



\### Configuration



\- Windows Server: `10.10.30.10/24`

\- Default Gateway: `10.10.30.1`

\- VLAN: 30 — Servers



\### Result



Windows Server successfully reached `10.10.30.1`.



This validated the path:



`Windows Server → GNS3 Switch → GNS3 Cloud → USB Ethernet → MASON-SW1 → MASON-R1`



\*\*Status: PASS\*\*



\---



\## 6. Ubuntu Server Gateway Connectivity



\### Objective



Verify that Ubuntu Server can communicate with its default gateway through the same physical/virtual infrastructure.



\### Configuration



\- Ubuntu Server: `10.10.30.20/24`

\- Default Gateway: `10.10.30.1`

\- VLAN: 30 — Servers



\### Result



Ubuntu Server successfully reached `10.10.30.1`.



\*\*Status: PASS\*\*



\---



\## 7. Server-to-Server Communication



\### Objective



Verify bidirectional communication between the Windows and Ubuntu servers.



\### Tests



Windows Server:



`10.10.30.10 → 10.10.30.20`



Ubuntu Server:



`10.10.30.20 → 10.10.30.10`



\### Result



After configuring the appropriate Windows Firewall rule, bidirectional communication was successful.



\*\*Status: PASS\*\*



\---



\## 8. Active Directory Domain Services



\### Objective



Verify successful deployment of the project's Active Directory environment.



\### Configuration



\- Domain: `masonmfg.internal`

\- NetBIOS Name: `MASONMFG`

\- Domain Controller: Windows Server 2025

\- Domain Controller Address: `10.10.30.10`

\- DNS Server: Enabled

\- Global Catalog: Enabled



\### Result



The server was successfully promoted as the first domain controller of the new forest.



Active Directory administrative tools became available after promotion and reboot.



\*\*Status: PASS\*\*



\---



\## 9. Active Directory DNS



\### Objective



Verify that DNS contains the records required for Active Directory service discovery.



\### Verified DNS Structure



The following Active Directory-integrated forward lookup zones were created:



\- `\_msdcs.masonmfg.internal`

\- `masonmfg.internal`



Service records were verified for:



\- Kerberos

\- LDAP

\- kpasswd

\- Global Catalog



\### Result



Active Directory DNS records were successfully created and verified.



\*\*Status: PASS\*\*



\---



\## 10. Reverse DNS



\### Objective



Verify reverse DNS functionality for the Mason server network.



\### Configuration



Reverse lookup zone:



`30.10.10.in-addr.arpa`



Network:



`10.10.30.0/24`



A PTR record was created for:



`10.10.30.10`



\### Validation



Reverse lookup testing was performed using:



`nslookup 10.10.30.10`



The query successfully returned the domain controller's hostname and address.



\### Result



Reverse DNS resolution is operational.



\*\*Status: PASS\*\*



\---



\## Validation Still Required



The following tests will be added as their corresponding project phases are implemented:



\- Domain client join and authentication

\- Active Directory user, group, and organizational unit validation

\- DHCP address assignment

\- DHCP relay between VLANs

\- DNS forwarding and external name resolution

\- FortiGate internal connectivity

\- Internet connectivity through FortiGate

\- Firewall policy validation

\- Mason-to-Troy endpoint communication

\- Legacy Windows XP connectivity

\- Legacy/OT ACL isolation

\- Legacy/OT Internet blocking

\- Authorized management access

\- Switch security and hardening controls

\- Centralized logging

\- Python/Netmiko automation

\- Configuration backup validation

\- Wireshark protocol analysis

\- End-to-end enterprise connectivity

\- End-to-end security testing



\## Validation Approach



Each major project phase follows the same general process:



\*\*Build → Verify Configuration → Test Connectivity or Service → Troubleshoot if Necessary → Retest → Document Results\*\*



A feature is not considered complete solely because its configuration exists. Expected behavior must also be demonstrated through testing.

