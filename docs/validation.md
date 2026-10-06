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

## 11. Windows Security Auditing

### Objective

Verify that Windows Advanced Audit Policy settings are applied through Group Policy and generate Security log events during controlled Active Directory activity.

### Validation

Advanced Audit Policy settings were verified using `auditpol`.

Controlled tests produced the following Windows Security events:

- Event ID 4768 — Kerberos authentication ticket request
- Event ID 4769 — Kerberos service ticket request
- Event ID 4738 — User account modification
- Event ID 4728 — Member added to a security-enabled global group
- Event ID 4729 — Member removed from a security-enabled global group
- Event ID 5136 — Active Directory object modification

Directory Service Changes auditing was additionally validated using a SACL applied to descendant user objects.

Computer Account Management auditing was policy-validated but was not intentionally triggered for event-level validation.

### Result

Advanced Audit Policy configuration and multiple security auditing categories were successfully validated through effective policy and Windows Security event evidence.

**Status: PASS**

---

## 12. Kea DHCP and DHCP Relay

### Objective

Verify centralized DHCP address assignment from the Mason Ubuntu Server to a client on the remote Troy employee VLAN.

### Configuration

- Kea DHCP Server: `10.10.30.20`
- Troy Employee Network: `10.20.20.0/24`
- Troy Gateway: `10.20.20.1`
- DHCP Relay: `ip helper-address 10.10.30.20`
- DNS Server: `10.10.30.10`
- DNS Suffix: `masonmfg.internal`

### Validation

TROY-WIN11-01 successfully received:

- IPv4 address: `10.20.20.103/24`
- Default gateway: `10.20.20.1`
- DHCP server: `10.10.30.20`
- DNS server: `10.10.30.10`
- DNS suffix: `masonmfg.internal`

The client successfully reached both its local gateway and Mason infrastructure across the routed WAN.

### Result

Centralized Kea DHCP and Cisco DHCP relay successfully provided network configuration to the remote Troy employee VLAN.

**Status: PASS**

---

## 13. FortiGate and Internet Connectivity

### Objective

Verify that internal enterprise traffic can reach external networks through the FortiGate Internet edge.

### Validation

Internet connectivity was successfully demonstrated from both Mason infrastructure and the Troy Windows client.

TROY-WIN11-01 successfully pinged:

`8.8.8.8`

with 0% packet loss after the required default route was propagated through OSPF.

External DNS resolution was also successfully validated through the internal Windows DNS infrastructure.

### Result

The enterprise network successfully reaches external destinations through the Mason routing and FortiGate Internet path.

**Status: PASS**

---

## 14. OSPF Default Route Propagation

### Objective

Verify that Troy dynamically receives an Internet default route from Mason through OSPF.

### Configuration

MASON-R1 contains a static default route toward the FortiGate and advertises the default route through OSPF using:

`default-information originate`

### Validation

TROY-SW1 successfully learned:

`O*E2 0.0.0.0/0 [110/1] via 10.255.0.1`

The gateway of last resort on TROY-SW1 became `10.255.0.1`.

After convergence, TROY-WIN11-01 successfully reached `8.8.8.8`.

### Result

OSPF default-route propagation from Mason to Troy is operational.

**Status: PASS**

---

## 15. Troy Domain Join and Authentication

### Objective

Verify that a workstation located at the Troy site can join the Mason Active Directory domain and authenticate a domain user across the routed WAN.

### Validation

TROY-WIN11-01 successfully joined:

`masonmfg.internal`

After rebooting, the Troy employee test account successfully authenticated to the workstation.

`gpresult` identified the domain controller and confirmed domain-based policy processing.

### Result

Active Directory domain membership and domain authentication across the Mason-Troy WAN were successfully validated.

**Status: PASS**

---

## 16. Troy User Group Policy

### Objective

Verify that user-side Group Policy settings linked to the Troy Users OU apply to a Troy employee account.

### Validation

After signing in as the Troy employee test account:

- `gpupdate /force` completed successfully.
- `gpresult /r` listed Troy Workstation Policy under Applied Group Policy Objects.
- Membership in the expected Troy and shared-resource security groups was confirmed.
- Attempting to access the Windows Run command produced a policy restriction message.

The configured Settings Page Visibility restriction for the Windows About page has not yet been successfully behaviorally validated and remains under investigation.

### Result

The Troy Workstation Policy is confirmed to apply to the Troy employee account, and the Run restriction has been behaviorally validated.

**Status: PASS — with one configured setting still under investigation**

---

## 17. Domain Workstation Security Baseline

### Objective

Verify that the shared computer security baseline applies to TROY-WIN11-01 after correct Active Directory OU placement.

### Validation

After moving TROY-WIN11-01 into:

`OU=Computers,OU=Troy,OU=MasonMFG,DC=masonmfg,DC=internal`

computer-scope `gpresult` showed:

- Domain Workstation Security Baseline
- Default Domain Policy

The configured machine inactivity limit was independently checked using the Windows registry.

`InactivityTimeoutSecs` returned:

`REG_DWORD 0x12c`

which corresponds to 300 seconds.

### Result

The Domain Workstation Security Baseline successfully applies to the Troy workstation, and the configured five-minute inactivity timeout was validated.

**Status: PASS**

---



## Validation Still Required

- Complete remaining Troy workstation GPO validation

- Validate Mason workstation domain join, authentication, and site-specific Group Policy

- Expand centralized Kea DHCP to additional Mason and Troy VLANs

- Validate domain file sharing across the Mason-Troy WAN

- Perform additional FortiGate firewall policy validation

- Integrate the legacy Windows XP/manufacturing endpoint

- Implement Legacy/OT VLAN isolation using extended ACLs

- Validate Legacy/OT isolation with before-and-after connectivity testing

- Validate authorized management access

- Implement and validate additional switch security and hardening controls

- Implement centralized logging and monitoring

- Develop and validate Python/Netmiko automation

- Validate automated configuration backup functionality

- Perform Wireshark protocol analysis

- Complete final end-to-end enterprise connectivity testing

- Complete final end-to-end security testing




\## Validation Approach



Each major project phase follows the same general process:



\*\*Build → Verify Configuration → Test Connectivity or Service → Troubleshoot if Necessary → Retest → Document Results\*\*



A feature is not considered complete solely because its configuration exists. Expected behavior must also be demonstrated through testing.

