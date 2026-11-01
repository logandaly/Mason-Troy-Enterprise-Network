# Project Milestones



This document tracks the implementation progress of the Mason-Troy Enterprise Network. Milestones are documented as the network is built, tested, and validated.



## Milestone 1 — Physical Network and VLAN Foundation



### Completed



- Assigned physical Cisco equipment to the Mason and Troy sites.

- Established Mason and Troy VLAN structures.

- Configured management, employee, server, and legacy/OT network segments.

- Configured VLAN 999 as a dedicated native VLAN.

- Configured Mason router-on-a-stick inter-VLAN routing.

- Configured Troy Layer 3 switching using SVIs.

- Validated local VLAN gateway connectivity.



### Design Decision



The two available Catalyst 3560 switches contained different IOS feature sets. The switch running Advanced IP Services was assigned to Troy because it supports the Layer 3 and OSPF functionality required by the design. The IP Base switch was assigned to Mason as a Layer 2 access switch.



This avoided an unnecessary IOS upgrade while making effective use of the available physical hardware.



---



## Milestone 2 — Mason-Troy WAN and OSPF



### Completed



- Converted TROY-SW1 Fa0/24 into a routed port.

- Configured the `10.255.0.0/30` point-to-point WAN.

- Assigned `10.255.0.1` to MASON-R1.

- Assigned `10.255.0.2` to TROY-SW1.

- Configured OSPF process 1 and Area 0.

- Established a full OSPF adjacency between Mason and Troy.

- Advertised the Mason and Troy VLAN networks through OSPF.

- Verified bidirectional dynamic route propagation.

- Saved validated Cisco configurations.



### Validation



MASON-R1 successfully learned the Troy networks through `10.255.0.2`, while TROY-SW1 successfully learned the Mason networks through `10.255.0.1`.



---



## Milestone 3 — Physical and Virtual Network Integration



### Completed



- Integrated the GNS3 virtual environment with the physical Mason network.

- Configured a GNS3 Ethernet switch with VLAN-aware access ports.

- Configured GNS3 switch port 12 as an 802.1Q trunk.

- Connected the trunk through a GNS3 Cloud interface to the host USB-to-Ethernet adapter.

- Converted MASON-SW1 Fa0/5 into an 802.1Q trunk.

- Allowed VLANs 10, 20, 30, and 999 across the physical/virtual trunk.

- Verified trunk operation and Spanning Tree forwarding state.

- Connected Windows Server and Ubuntu Server to Mason VLAN 30.

- Verified virtual server connectivity through the physical Cisco infrastructure.



### Troubleshooting



Initial virtual-to-physical connectivity failed because the host USB-to-Ethernet adapter still contained an old static Troy address of `10.20.30.10`.



The stale address was removed, allowing the adapter to operate strictly as part of the Layer 2 bridge. After the change, the virtual Windows Server successfully reached the Mason VLAN 30 gateway at `10.10.30.1`.



This validated the complete path between the GNS3 virtual environment and the physical Mason network.



---



## Milestone 4 — Server Infrastructure



### Completed



- Deployed Windows Server 2025 in the GNS3 environment.

- Configured Windows Server with static address `10.10.30.10/24`.

- Configured default gateway `10.10.30.1`.

- Deployed Ubuntu Server in the GNS3 environment.

- Configured Ubuntu Server with static address `10.10.30.20/24`.

- Configured default gateway `10.10.30.1`.

- Connected both servers to Mason VLAN 30.

- Verified both servers could reach the Mason VLAN 30 gateway.

- Verified bidirectional communication between Windows Server and Ubuntu Server.



### Troubleshooting



Initial testing showed that Windows Server could successfully ping Ubuntu Server, but Ubuntu Server could not successfully ping Windows Server.



Network routing and VLAN connectivity were functioning correctly. Investigation identified Windows Firewall as the source of the asymmetric connectivity.



The built-in File and Printer Sharing firewall rule group was enabled to permit the required inbound ICMP traffic while leaving Windows Firewall enabled.



After the change, Ubuntu Server successfully reached Windows Server, confirming bidirectional server communication.



---



## Milestone 5 — Active Directory and DNS



### Completed



- Installed Active Directory Domain Services (AD DS) on Windows Server 2025.

- Installed the Windows DNS Server role.

- Promoted the server as the first domain controller in a new Active Directory forest.

- Created the `masonmfg.internal` domain.

- Configured the `MASONMFG` NetBIOS domain name.

- Enabled DNS Server and Global Catalog functionality on the domain controller.

- Verified the Active Directory-integrated DNS zones.

- Verified automatically generated Kerberos, LDAP, kpasswd, and Global Catalog SRV records.

- Created an IPv4 reverse lookup zone for the Mason server network.

- Configured the reverse lookup zone to use secure dynamic updates.

- Created and validated a PTR record for the domain controller at `10.10.30.10`.

- Successfully validated reverse DNS resolution using `nslookup`.



### Validation



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

The Troy Workstation Policy's Settings Page Visibility restriction was successfully validated on October 16, 2026.

After enabling the previously disabled Troy Computers OU policy link and restoring domain controller connectivity, Group Policy processing completed successfully.

While signed in as `MASONMFG\test.employee` on `TROY-WIN11-01`, Windows Settings → System no longer displayed the About page, confirming enforcement of `hide:about`.

Both the Troy Run command restriction and the About-page visibility restriction have now been behaviorally validated.


---

## Milestone 11 — Centralized Kea DHCP Expansion

### Completed

- Expanded the centralized Kea DHCPv4 configuration on Ubuntu Server (`10.10.30.20`) to support six VLAN subnets across the Mason and Troy sites.
- Configured DHCP address pools from `.100` through `.150` for all six subnets.
- Configured the appropriate VLAN default gateway for each DHCP scope.
- Configured all six scopes to distribute the Active Directory DNS server at `10.10.30.10`.
- Verified DHCP subnet definitions, pools, gateway options, and DNS options directly from the Kea configuration.
- Demonstrated successful DHCP assignment to the Mason Windows 11 workstation.
- Demonstrated DHCP assignment to a GNS3 test client on Mason VLAN 30.
- Previously validated DHCP relay and lease assignment to the Troy Windows 11 workstation across the routed WAN.

### Validation

The following DHCP client tests have been completed:

- **Troy VLAN 20:** `TROY-WIN11-01` received `10.20.20.103/24` from the centralized Kea server.
- **Mason VLAN 20:** `MASON-WIN11-01` successfully received a valid DHCP lease after restoration of the GNS3 server connection.
- **Mason VLAN 30:** A GNS3 test client received `10.10.30.100/24` and successfully pinged both the Ubuntu DHCP server and Windows domain controller.

All six DHCP scopes were successfully validated through client-side DHCP testing across the Mason and Troy VLANs. GNS3 VPC testing confirmed successful address assignment, and additional Windows 11 endpoint testing provided supporting evidence. Photographic evidence of the six-VLAN validation is documented in docs/validation.md.


### Troubleshooting

During Mason workstation integration, DHCP requests initially failed because of a stale GNS3 connection between the Ubuntu server and the virtual network.

Packet capture showed DHCP Discover traffic leaving the workstation without a corresponding DHCP Offer.

The router's VLAN 20 subinterface and DHCP relay configuration were checked and found correct.

Disconnecting and reconnecting the affected GNS3 link restored connectivity to Kea, allowing the workstation to obtain a valid DHCP lease.

This demonstrated the importance of validating Layer 2 connectivity and DHCP relay paths before assuming a DHCP service configuration failure.

### Supporting Evidence

Detailed scope information and screenshots are available in [IP Addressing and VLAN Plan](ip-vlan-plan.md).

---

## Milestone 12 — Mason Windows 11 Workstation Integration

### Completed

- Created a separate Windows 11 Pro virtual workstation for the Mason corporate site.
- Created an independent Mason QCOW2 base disk from the verified Troy workstation backup.
- Configured a dedicated Mason GNS3 QEMU template with UEFI and SATA disk support.
- Used Windows Sysprep to generalize the cloned installation and avoid duplicate workstation identity issues.
- Completed Windows 11 setup and configured the workstation as `MASON-WIN11-01`.
- Connected the workstation to Mason VLAN 20.
- Successfully obtained network configuration through centralized Kea DHCP.
- Joined the workstation to the `masonmfg.internal` Active Directory domain.
- Moved its computer object into the Mason Computers organizational unit.
- Successfully authenticated using the Mason domain account `MASONMFG\test.manager`.
- Confirmed application of the Domain Workstation Security Baseline.

### Troubleshooting

The initial Mason workstation failed to boot correctly and entered the UEFI shell.

Investigation identified problems with the QEMU template's disk image reference and disk interface configuration. The copied template initially referenced the Troy base image and launched the disk using IDE instead of the SATA/AHCI configuration required by the working installation.

A separate Mason base image was created and validated using `qemu-img check` and `qemu-img info`. The Mason template was corrected to reference this independent disk.

After correcting the QEMU configuration, the workstation successfully booted.

The cloned Windows installation initially retained Troy's domain identity. To prevent conflicts, the original Troy workstation remained powered off while the Mason installation was generalized using Sysprep.

During Mason VLAN 20 integration, DHCP initially failed because of a stale GNS3 connection to the Ubuntu DHCP server. Restoring the affected virtual link allowed the workstation to obtain its lease and proceed with domain integration.

### Validation

The following results were confirmed:

- `MASON-WIN11-01` successfully joined `masonmfg.internal`.
- Domain authentication succeeded using `MASONMFG\test.manager`.
- The computer object was placed in `OU=Computers,OU=Mason,OU=MasonMFG,DC=masonmfg,DC=internal`.
- Computer-scope `gpresult /r` confirmed application of the Domain Workstation Security Baseline and Default Domain Policy.
- User-scope `gpresult /r` confirmed domain authentication context and membership in the Mason-Employees and Shared-Resources-Group security groups.

Mason-specific user Group Policy configuration and behavioral validation remain pending. No unverified Mason-specific policy enforcement is claimed.

### Significance

This milestone established an independently configured Windows 11 workstation at the Mason site, complementing the previously deployed Troy workstation.

Both sites now have domain-joined endpoints capable of using centralized Active Directory authentication and computer security policies.

The troubleshooting process also demonstrated practical experience with QEMU disk images, virtualization templates, Windows Sysprep, DHCP relay, and Active Directory computer management.




---

## Milestone 13 — Cross-Site File Sharing and Windows Server Security Validation

### Completed

- Verified Active Directory organizational units for Mason and Troy.
- Confirmed Mason and Troy test-user membership in Shared-Resources-Group.
- Verified NTFS Modify, Read, and Write permissions on CompanyShare.
- Verified SMB share-level Change and Read permissions.
- Successfully mapped CompanyShare from the Troy Windows 11 workstation.
- Modified a shared file from Troy and verified the changes on Mason Windows Server.
- Confirmed Windows Security Event 4624 for the Troy employee account.
- Verified Network Logon Type 3 and source address `10.20.20.100`.
- Confirmed successful Kerberos service ticket auditing through Event ID 4769.
- Verified Success and Failure logon auditing using `auditpol`.
- Confirmed enabled workstation GPO links for Mason and Troy.
- Confirmed the Windows Security Auditing Policy link on the Domain Controllers OU.
- Verified internal Active Directory DNS records for Mason and Troy.
- Verified external DNS resolution through the Mason DNS server.

### Validation

The Troy workstation successfully accessed the Mason CompanyShare resource using domain authentication.

A shared file was modified from Troy, and the changes were subsequently verified on the Mason Windows Server.

Active Directory group membership and both NTFS and SMB share permissions were inspected to confirm the configured access controls.

Windows Security Event 4624 confirmed successful network authentication by `MASONMFG\test.employee` from the Troy workstation.

Kerberos Event 4769 and the effective Windows audit policy provided additional authentication and auditing evidence.

External DNS resolution was validated using:

`nslookup google.com 10.10.30.10`

### Outstanding Items

- The original direct UNC navigation restriction remains unexplained, although mapped-drive access and file modification are working.
- Windows Security Event ID 4625 was subsequently observed and validated, confirming failed-logon auditing behavior.
- Troy Legacy/OT VLAN 30 isolation and FortiGate firewall policy testing were completed in later project phases and are documented separately.
- Additional FortiGate management hardening, unresolved transit connectivity troubleshooting, and network automation remain future work.
### Result

**Status: PASS — Cross-site SMB access, authentication auditing, DNS, and security configuration validation**

The enterprise now has documented evidence of centrally managed user identities, group-based file permissions, cross-site resource access, security event logging, and DNS services.

Supporting screenshots and detailed test results are recorded in [Network Validation](validation.md).

---

## Milestone 14 — Troy Legacy/OT VLAN 30 Isolation

### Completed

- Configured extended ACLs on TROY-SW1 to isolate the Legacy/OT network (`10.20.30.0/24`).
- Applied `TROY-OT-IN` to restrict traffic originating from VLAN 30.
- Applied `TROY-OT-OUT` to restrict routed traffic entering VLAN 30.
- Established a default-deny approach for unauthorized routed communication.
- Preserved local Layer 2 communication within the Legacy/OT VLAN.
- Captured before-and-after connectivity evidence.
- Verified ACL enforcement through controlled connectivity testing and deny counters.

### Validation

Before ACL deployment, the Legacy/OT test environment could communicate with the Mason server infrastructure.

After deployment, controlled tests confirmed that unauthorized routed communication between the Legacy/OT network and other enterprise networks was blocked.

ACL deny counters increased during testing, providing additional evidence that traffic matched the configured restrictions.

### Validation Limitations

- DHCP successfully assigned addresses to Troy VLAN 30 clients before ACL deployment.
- DHCP functionality after ACL deployment has not been independently validated.
- Local Layer 2 communication within VLAN 30 is not filtered by the routed ACLs.
- The testing does not establish comprehensive protection against every possible network attack.

### Result

**Status: PASS — Bidirectional routed Legacy/OT isolation validated.**

Supporting screenshots and test results are documented in [Network Validation](validation.md).

---

## Milestone 15 — FortiGate Firewall Policy Enforcement and Logging

### Completed

- Configured FortiGate firewall policies to control traffic crossing the enterprise security boundary.
- Validated permitted traffic through controlled connectivity testing.
- Validated denied traffic through controlled connectivity testing.
- Inspected firewall policy hit counters to identify traffic matching configured policies.
- Reviewed FortiGate traffic logs to verify visibility into firewall activity.
- Captured firewall policy configurations, traffic tests, counters, and logging evidence.

### Validation

Controlled testing demonstrated that the configured FortiGate policies permitted authorized traffic and denied restricted traffic.

Firewall policy counters provided supporting evidence of traffic matching the configured rules.

Before-and-after screenshots showed changes in policy counters. These changes demonstrate traffic activity but do not independently prove that firewall configurations were modified between captures.

FortiGate traffic logs provided additional visibility into policy enforcement.

### Validation Limitations

- The dedicated Mason-to-FortiGate transit network (`10.10.40.0/30`) subsequently experienced an unresolved ARP connectivity failure.
- Earlier successful Internet connectivity tests remain valid historical evidence, but current end-to-end connectivity requires revalidation.
- The separate FortiGate VMnet1 management connectivity investigation remains unresolved.
- Firewall policy validation does not establish that every possible traffic scenario has been tested.

### Result

**Status: PASS — FortiGate firewall policy enforcement and logging validated for the tested traffic scenarios.**

**Outstanding:** Revalidate the Mason-to-FortiGate transit connection and investigate the separate VMnet1 management connectivity issue.

Supporting screenshots and test results are documented in [Network Validation](validation.md). Additional investigation details are recorded in [Troubleshooting](troubleshooting.md).

---

## Milestone 16 — Troy Switch Security Hardening

### Completed

- Configured port security on 12 TROY-SW1 access ports.
- Set the maximum permitted MAC addresses to one per protected port.
- Configured port security violation mode as `restrict`.
- Enabled PortFast on designated access ports.
- Configured BPDU Guard on designated access ports.
- Enabled SSH version 2 for encrypted remote switch administration.
- Disabled HTTP and HTTPS management services.
- Captured switch configuration and operational verification evidence.

### Validation

Cisco IOS configuration and verification commands confirmed the implemented security controls.

Port security settings were verified on the configured access ports, including the maximum MAC address limit and violation mode.

PortFast and BPDU Guard configuration was inspected to confirm the intended access-port protections.

SSH management configuration and operational status were verified.

HTTP and HTTPS management services were confirmed disabled.

### Validation Limitations

The following behavioral tests were not independently completed:

- Connecting an unauthorized device to trigger a port security violation.
- Introducing a BPDU to verify BPDU Guard enforcement.
- Attempting a Telnet connection to confirm rejection.

These controls are configuration-validated but should not be described as behaviorally validated.

### Result

**Status: PASS — Troy switch security hardening configuration verified.**

**Outstanding:** Optional behavioral enforcement testing.

Supporting screenshots and command output are documented in [Network Validation](validation.md).
