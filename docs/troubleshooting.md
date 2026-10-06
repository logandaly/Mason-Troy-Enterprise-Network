\# Troubleshooting



This document records significant technical problems encountered during the implementation of the Mason-Troy Enterprise Network. Each case documents the symptoms, investigation, root cause, resolution, and validation process.



\## Case 1 — GNS3 Virtual Servers Unable to Reach Physical Network



\### Problem



Virtual servers connected through GNS3 were unable to successfully communicate with the physical Mason network through the USB-to-Ethernet bridge.



\### Symptoms



\- Physical Cisco interfaces and trunks appeared operational.

\- The GNS3 virtual switch and Cloud connection were configured.

\- The Windows Server could not successfully reach its default gateway at `10.10.30.1`.

\- Connectivity failed despite the expected VLAN 30 path being configured.



\### Investigation



The physical and virtual Layer 2 path was checked first, including:



\- GNS3 virtual switch configuration

\- 802.1Q trunk configuration

\- MASON-SW1 Fa0/5

\- VLAN 30 availability

\- Physical USB-to-Ethernet connectivity



The host's USB-to-Ethernet adapter was then inspected and found to still have an old static address of `10.20.30.10` from earlier Troy testing.



\### Root Cause



The USB-to-Ethernet adapter retained an outdated Layer 3 configuration while being repurposed as a Layer 2 bridge between GNS3 and the physical Mason switch.



\### Resolution



The stale `10.20.30.10` address was removed from the USB-to-Ethernet adapter. The adapter was left without a manually configured lab IP address so it could function as part of the Layer 2 bridge.



\### Validation



After removing the stale address, Windows Server successfully reached the Mason VLAN 30 gateway at `10.10.30.1`.



This confirmed successful communication across the complete path:



`Windows Server → GNS3 Switch → GNS3 Cloud → USB Ethernet → MASON-SW1 → MASON-R1`



\### Lesson Learned



When repurposing a physical network interface for Layer 2 bridging, old Layer 3 configuration should be checked early in the troubleshooting process. Physical link and trunk status alone do not guarantee that the host interface is correctly configured for its new role.



\## Case 2 — Asymmetric Communication Between Windows and Ubuntu Servers



\### Problem



Ubuntu Server was unable to successfully ping Windows Server even though both systems were connected to Mason VLAN 30.



\### Symptoms



\- Windows Server could successfully ping Ubuntu Server.

\- Ubuntu Server could not successfully ping Windows Server.

\- Both servers could reach the VLAN 30 default gateway at `10.10.30.1`.

\- Both systems were configured within the `10.10.30.0/24` subnet.



\### Investigation



Because both servers could reach their gateway and Windows Server could initiate communication with Ubuntu Server, the VLAN, trunk, and routing infrastructure were already functioning.



The asymmetric behavior suggested that the problem was located on the Windows Server itself rather than within the Cisco network.



Windows Firewall was investigated as a possible source of the blocked inbound traffic.



\### Root Cause



Windows Firewall was blocking inbound ICMP echo requests from Ubuntu Server.



\### Resolution



The built-in Windows \*\*File and Printer Sharing\*\* firewall rule group was enabled rather than disabling Windows Firewall entirely.



This allowed the required inbound ICMP traffic while preserving host firewall protection.



\### Validation



After enabling the appropriate firewall rules:



\- Windows Server successfully pinged Ubuntu Server.

\- Ubuntu Server successfully pinged Windows Server.

\- Both servers successfully reached `10.10.30.1`.



Bidirectional communication between the two Mason servers was confirmed.



\### Lesson Learned



Successful one-way communication is an important troubleshooting clue. When one host can initiate communication but the other cannot, host-based security controls should be investigated before making unnecessary changes to switching or routing infrastructure.



\---



\## Case 3 — OSPF Unavailable on Original Troy Switch



\### Problem



The Catalyst 3560 originally assigned to Troy needed to perform Layer 3 routing and participate in OSPF, but OSPF could not be configured successfully.



\### Symptoms



The Cisco IOS command-line interface displayed OSPF as an available routing protocol when examining routing configuration options.



However, attempting to create an OSPF process resulted in an error indicating that the protocol was not available in the installed IOS image.



\### Investigation



The installed IOS images and feature sets on both available Catalyst 3560 switches were examined.



The original Troy switch was running an older IP Base image, while the original Mason switch was running an Advanced IP Services image.



The Advanced IP Services switch provided the Layer 3 routing and OSPF capabilities required by the Troy design.



An IOS upgrade was considered, including backing up the existing image and potentially transferring another image using TFTP.



\### Root Cause



The IP Base IOS image installed on the original Troy switch did not provide the required OSPF functionality.



The presence of OSPF-related command options in the CLI did not guarantee that the installed image supported actually running the protocol.



\### Resolution



Instead of performing an unnecessary IOS upgrade, the roles of the two physical Catalyst 3560 switches were exchanged.



The Advanced IP Services switch became `TROY-SW1` and was assigned the Layer 3 and OSPF responsibilities.



The IP Base switch became `MASON-SW1` and was configured as a Layer 2 access switch.



\### Validation



After the role change:



\- TROY-SW1 successfully enabled IP routing.

\- OSPF process 1 was successfully configured.

\- TROY-SW1 formed a full OSPF adjacency with MASON-R1.

\- Mason and Troy routes were successfully exchanged.

\- Bidirectional communication across the WAN was validated.



\### Lesson Learned



Hardware and software capabilities should be verified before changing network architecture or performing firmware upgrades. Reassigning existing equipment according to its capabilities can sometimes provide a simpler and lower-risk solution.



\---



\## Case 4 — GNS3 Packet Capture Library Error



\### Problem



The GNS3 Ethernet switch reported that `wpcap.dll` could not be found, preventing the Windows packet capture components from functioning as expected.



\### Symptoms



GNS3 displayed an error indicating that `wpcap.dll` was missing.



Npcap was already installed, and the DLL existed within the Npcap installation directory, but GNS3 was still unable to use the expected WinPcap-compatible interface.



\### Investigation



The Windows Npcap installation was checked.



The packet capture library existed within the Npcap directory, indicating that the software itself was installed. The issue appeared to involve compatibility between the Npcap installation and software expecting the older WinPcap API.



Rather than manually copying DLL files into Windows system directories, the official Npcap installer was used to correct the installation.



\### Root Cause



Npcap had not been installed with the WinPcap API compatibility option required by the affected GNS3 component.



\### Resolution



Npcap was reinstalled using the official installer with:



\*\*Install Npcap in WinPcap API-compatible Mode\*\*



enabled.



Manual DLL copying was avoided.



\### Validation



After reinstalling Npcap with compatibility mode enabled, the environment was able to proceed with the GNS3 Ethernet switching and physical bridging configuration without the previous blocking issue.



\### Lesson Learned



When troubleshooting software dependencies, reinstalling or correcting the supported compatibility configuration is preferable to manually copying system libraries. This reduces the risk of introducing unsupported or inconsistent DLL versions.



\---

## Case 5 — Troy Client Unable to Reach the Internet

### Problem

TROY-WIN11-01 successfully received network configuration from the centralized Kea DHCP server and could communicate with internal Mason resources, but it could not reach the Internet.

### Symptoms

- TROY-WIN11-01 received a valid `10.20.20.0/24` DHCP lease.
- The client successfully reached its default gateway at `10.20.20.1`.
- The client successfully reached Mason infrastructure across the WAN.
- A ping to `8.8.8.8` failed.
- A traceroute stopped at the Troy default gateway.
- TROY-SW1 reported that no gateway of last resort was configured.

### Investigation

Because DHCP, local gateway connectivity, and intersite routing were already functioning, troubleshooting focused on the route from Troy toward external networks.

The routing table on TROY-SW1 showed OSPF routes for the Mason networks but no default route.

MASON-R1 was then checked and already contained a static default route toward the FortiGate at `10.10.40.1`.

This showed that Mason had an Internet path, but the default route was not being propagated to Troy through OSPF.

### Root Cause

MASON-R1 had a valid static default route toward the FortiGate, but OSPF process 1 was not advertising that default route to TROY-SW1.

### Resolution

The following command was added under OSPF process 1 on MASON-R1:

`default-information originate`

After OSPF convergence, TROY-SW1 learned:

`O*E2 0.0.0.0/0 [110/1] via 10.255.0.1`

### Validation

After the routing change:

- TROY-SW1 displayed `10.255.0.1` as its gateway of last resort.
- TROY-WIN11-01 successfully pinged `8.8.8.8` with 0% packet loss.
- Internal Mason-Troy connectivity continued to function normally.

This validated the complete Troy-to-Internet routing path through MASON-R1 and FortiGate.

### Lesson Learned

Dynamic routing between internal networks does not automatically provide downstream routers or Layer 3 switches with an Internet default route. Default-route propagation must be explicitly designed and verified.

---

## Case 6 — Workstation Security Baseline Did Not Apply to Troy Client

### Problem

TROY-WIN11-01 successfully joined `masonmfg.internal`, and the Troy user policy applied correctly, but the Domain Workstation Security Baseline did not appear in the computer-scope Group Policy results.

### Symptoms

- `MASONMFG\test.employee` successfully authenticated to TROY-WIN11-01.
- `gpupdate /force` completed successfully.
- The Troy Workstation Policy appeared in the user's applied Group Policy Objects.
- `gpresult /scope computer /r` showed only Default Domain Policy.
- Domain Workstation Security Baseline was missing.

### Investigation

The computer-scope `gpresult` output was inspected to determine the Active Directory location of TROY-WIN11-01.

The workstation appeared as:

`CN=TROY-WIN11-01,CN=Computers,DC=masonmfg,DC=internal`

The Domain Workstation Security Baseline was linked to the Troy Computers OU rather than the domain's default Computers container.

Active Directory Users and Computers confirmed that the newly joined workstation had been automatically placed in the default Computers container.

### Root Cause

TROY-WIN11-01 was outside the organizational unit to which the Domain Workstation Security Baseline was linked.

The GPO itself was functioning correctly, but the computer object was not within its scope.

### Resolution

TROY-WIN11-01 was moved in Active Directory to:

`OU=Computers,OU=Troy,OU=MasonMFG,DC=masonmfg,DC=internal`

Group Policy was then refreshed on the workstation.

### Validation

After the move and policy refresh:

- `gpresult /scope computer /r` showed the correct Troy Computers OU.
- Domain Workstation Security Baseline appeared under Applied Group Policy Objects.
- `InactivityTimeoutSecs` returned `REG_DWORD 0x12c`, confirming the configured 300-second inactivity timeout.
- The existing Troy user policy continued to function.

### Lesson Learned

Successful domain membership does not guarantee that an endpoint is located in the correct Active Directory OU. Because GPO scope depends on directory placement and linking, computer-object location should be verified when an expected policy does not apply.

---

## Case 7 — Troy Domain Join Initially Unable to Locate Domain Controller

### Problem

TROY-WIN11-01 initially reported that an Active Directory Domain Controller for `masonmfg.internal` could not be contacted during the domain-join process.

### Symptoms

- The Troy client had working routed connectivity.
- Internet connectivity was operational.
- The client was configured to use `10.10.30.10` as its DNS server.
- An Active Directory SRV lookup timed out against `10.10.30.10`.
- The initial domain-join attempt could not locate a domain controller.

### Investigation

DNS connectivity was tested separately from general network connectivity.

From TROY-WIN11-01:

`Test-NetConnection 10.10.30.10 -Port 53`

returned:

`TcpTestSucceeded : True`

This proved that the Troy client could reach the Windows DNS server over TCP port 53 from its `10.20.20.0/24` network.

No network or firewall configuration was changed solely on the basis of the initial DNS timeout. Domain-controller discovery was retested, and the domain join subsequently became available.

During the join process, the normal Troy employee test account was also distinguished from the domain administrator account authorized to perform the join.

### Root Cause

A definitive root cause for the temporary DNS/SRV lookup timeout was not established.

The available evidence confirmed IP connectivity and TCP port 53 reachability to the DNS server, so no unsupported root-cause claim was made.

### Resolution

Domain-controller discovery was retested after connectivity verification. TROY-WIN11-01 was then successfully joined to `masonmfg.internal` using authorized domain administrator credentials.

### Validation

After joining the domain:

- `MASONMFG\test.employee` successfully authenticated to TROY-WIN11-01.
- Group Policy processing completed successfully.
- The workstation communicated with the domain controller and received domain policies.

### Lesson Learned

A temporary service-discovery failure should not immediately be attributed to routing or firewall configuration. Testing the specific service path first can prevent unnecessary network changes. Troubleshooting documentation should also distinguish a confirmed root cause from a problem that disappeared before its exact cause could be established.




\## Troubleshooting Methodology



The project uses a structured troubleshooting process when connectivity or service problems occur:



1\. Identify the symptoms and determine the expected behavior.

2\. Verify physical connectivity and interface state.

3\. Verify VLAN membership and trunk configuration.

4\. Verify IP addressing and default gateways.

5\. Verify routing and routing protocol operation.

6\. Test connectivity incrementally across the traffic path.

7\. Investigate host firewalls and application services when network connectivity is otherwise functional.

8\. Make one controlled change at a time.

9\. Retest after each significant change.

10\. Document the root cause, resolution, and validation results.



This approach helps distinguish Layer 1, Layer 2, Layer 3, host, and application problems without making unnecessary configuration changes.