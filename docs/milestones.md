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



---

## Milestone 6 — Active Directory Organization, Group Policy, and Security Auditing

### Completed

- Created the `MasonMFG` organizational structure in Active Directory.
- Created separate Mason and Troy organizational units for users, computers, and servers.
- Created test domain user accounts for Mason and Troy validation.
- Created security groups for employee and shared-resource access.
- Created and linked the Troy Workstation Policy.
- Created and linked the Domain Workstation Security Baseline.
- Configured Windows Advanced Audit Policy through Group Policy.
- Enabled auditing for Kerberos authentication and service ticket activity.
- Enabled auditing for user and security group account management.
- Enabled Directory Service Changes auditing.
- Configured an Active Directory SACL to audit changes to descendant user objects.
- Validated security auditing through Windows Security event logs.

### Validation

Advanced Audit Policy settings were verified with `auditpol`. Controlled tests generated and validated Windows Security events including Kerberos authentication, Kerberos service ticket requests, user account changes, security group membership changes, and Active Directory object modifications.

This established centralized security policy enforcement and auditing through Active Directory and Group Policy.

---

## Milestone 7 — FortiGate Internet Edge

### Completed

- Integrated a FortiGate virtual firewall with the Mason network.
- Established the routed transit path between MASON-R1 and FortiGate.
- Configured a default route from MASON-R1 toward the FortiGate.
- Configured FortiGate routing toward the internal enterprise networks.
- Configured an internal-to-Internet firewall policy with NAT.
- Verified Internet connectivity from the Mason network.
- Verified external DNS resolution through the Windows DNS infrastructure.

### Validation

MASON-R1 and the Mason Windows Server successfully reached external Internet destinations. Internal Active Directory DNS continued to resolve `masonmfg.internal`, while external DNS queries were successfully forwarded for public name resolution.

---

## Milestone 8 — Centralized Kea DHCP and Troy Endpoint Connectivity

### Completed

- Installed and configured Kea DHCP on Ubuntu Server at `10.10.30.20`.
- Configured DHCP service for the Troy employee network.
- Configured DHCP relay on TROY-SW1 VLAN 20 using `ip helper-address 10.10.30.20`.
- Connected TROY-WIN11-01 to the Troy employee VLAN.
- Successfully assigned a DHCP lease across the routed Mason-Troy network.
- Supplied the Troy client with its default gateway, Active Directory DNS server, and domain suffix.
- Verified connectivity from the Troy client to the Troy gateway and Mason server infrastructure.

### Validation

TROY-WIN11-01 received:

- IPv4 address: `10.20.20.103/24`
- Default gateway: `10.20.20.1`
- DHCP server: `10.10.30.20`
- DNS server: `10.10.30.10`
- DNS suffix: `masonmfg.internal`

This demonstrated centralized DHCP operation across the routed Mason-Troy WAN using DHCP relay.

---

## Milestone 9 — Troy Internet Routing and OSPF Default Route

### Troubleshooting

Although TROY-WIN11-01 could communicate with internal Mason resources, initial Internet testing failed. A traceroute stopped at the Troy default gateway, and TROY-SW1 reported that no gateway of last resort was configured.

MASON-R1 already contained a static default route toward the FortiGate at `10.10.40.1`, but that default route was not being advertised to Troy.

### Resolution

OSPF process 1 on MASON-R1 was configured with:

`default-information originate`

TROY-SW1 subsequently learned:

`O*E2 0.0.0.0/0 via 10.255.0.1`

### Validation

After OSPF convergence, TROY-WIN11-01 successfully pinged `8.8.8.8` with 0% packet loss.

This validated the complete path from the Troy employee network through TROY-SW1, the Mason-Troy WAN, MASON-R1, FortiGate, and the external network.

---

## Milestone 10 — Troy Domain Join and Group Policy Validation

### Completed

- Joined TROY-WIN11-01 to `masonmfg.internal`.
- Successfully authenticated to the workstation using the Troy domain test account.
- Forced Group Policy processing with `gpupdate /force`.
- Verified the Troy Workstation Policy using `gpresult`.
- Identified that the workstation computer object had initially been created in the default Active Directory `Computers` container.
- Moved TROY-WIN11-01 into `MasonMFG → Troy → Computers`.
- Refreshed Group Policy after correcting the computer object's OU placement.
- Verified application of the Domain Workstation Security Baseline.
- Validated the configured 300-second machine inactivity timeout.
- Behaviorally validated the Troy policy that restricts access to the Run command.

### Troubleshooting

The Domain Workstation Security Baseline initially did not appear in the computer-scope Resultant Set of Policy.

`gpresult /scope computer /r` showed that TROY-WIN11-01 was located in the default:

`CN=Computers,DC=masonmfg,DC=internal`

Because the security baseline was linked to the Troy Computers OU, the workstation was outside the GPO's intended scope.

The computer object was moved to:

`OU=Computers,OU=Troy,OU=MasonMFG,DC=masonmfg,DC=internal`

After Group Policy was refreshed, the Domain Workstation Security Baseline successfully appeared under the applied computer policies.

### Validation

The following endpoint controls were validated:

- Troy Workstation Policy applied to the Troy employee user.
- Domain Workstation Security Baseline applied to TROY-WIN11-01.
- `InactivityTimeoutSecs` returned `0x12c`, confirming the configured 300-second inactivity limit.
- Access to the Windows Run command was blocked by policy.

The configured Settings Page Visibility restriction for the Windows About page is still under investigation and is not considered validated.


