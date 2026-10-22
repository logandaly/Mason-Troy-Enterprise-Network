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



---

## Case 8 — Unexpected Windows Server VM Shutdowns

### Problem

The Windows Server 2025 virtual machine hosting Active Directory Domain Services and DNS experienced repeated unexpected shutdowns during the Mason–Troy network implementation.

In some instances, GNS3 continued displaying the Windows Server node as running even though the QEMU process was no longer accessible through VNC.

### Symptoms

- Windows Server unexpectedly became unavailable.
- GNS3 occasionally displayed the VM as running despite the guest being inaccessible.
- VNC connection attempts sometimes failed.
- The shutdowns initially appeared graceful but required further investigation.

### Investigation

Windows Event Viewer was used to examine the System event log.

The investigation identified:

- **Event ID 41 — Kernel-Power:** Windows reported that the system had restarted without a clean shutdown.
- **Event ID 6008 — EventLog:** Windows recorded an unexpected previous shutdown.
- **Event ID 1074:** No corresponding normal shutdown initiator was identified.
- **Event ID 1001:** No corresponding Windows bugcheck event was identified.

The virtual machine was configured with:

- 6144 MB RAM
- 2 virtual CPUs
- QEMU virtualization hosted within the GNS3 VM

Windows host event logs and GNS3 Doctor were also examined without identifying an obvious related failure.

### Findings

The Windows event logs confirmed that the shutdowns were unexpected rather than normal administrator-initiated shutdowns.

The absence of corresponding bugcheck evidence made an ordinary Windows blue-screen failure less evident.

The investigation therefore shifted toward the virtualization environment, including QEMU, GNS3 VM, and VMware.

**A definitive root cause was not established.**

### Resolution Status

Unresolved.

No specific virtualization component has been confirmed responsible, and no permanent corrective action has been validated.

### Next Troubleshooting Steps

If the problem occurs again:

1. Do not immediately restart the Windows Server VM.
2. Determine whether the VMware-hosted GNS3 VM is still running.
3. Check whether the Windows Server QEMU node is actually running or whether GNS3 is reporting an inaccurate status.
4. Collect relevant virtualization logs before restarting the affected component.
5. Compare the findings with the Windows System event logs.

### Lesson Learned

A virtual machine appearing operational in a network simulation interface does not guarantee that its underlying QEMU process or guest operating system is functioning.

Troubleshooting should examine the guest operating system, virtualization process, and hypervisor separately.

Unexpected shutdown events provide useful diagnostic evidence, but they do not independently establish the underlying root cause.



---

## Case 9 — Troy Workstation Group Policy Link Disabled

### Problem

The Troy Workstation Policy was intended to restrict access to the Windows Settings About page on `TROY-WIN11-01`, but the restriction was not taking effect.

The policy's user-side Run command restriction had previously been validated successfully.

### Symptoms

- The Troy Workstation Policy appeared in user-scope Group Policy results.
- The Run command restriction functioned as expected.
- The Windows Settings About page remained accessible.
- The computer-side Settings Page Visibility restriction had not been successfully validated.

### Investigation

Group Policy Management was used to inspect the Troy Workstation Policy.

The Settings Page Visibility configuration was found under:

`Computer Configuration → Policies → Administrative Templates → Control Panel`

The setting was enabled with the value:

`hide:about`

The corresponding setting under User Configuration was Not Configured.

Further inspection of the Active Directory organizational unit links revealed that the Troy Workstation Policy link at:

`MasonMFG → Troy → Computers`

was present but disabled.

The Domain Workstation Security Baseline link at the same OU was enabled.

### Root Cause

The Troy Workstation Policy's computer-side Settings Page Visibility restriction was outside the effective scope of the Troy workstation because the relevant GPO link to the Computers OU was disabled.

The working user-side restriction did not establish that the computer-side settings were also applying.

### Corrective Action

The existing Troy Workstation Policy link on the Troy Computers OU was enabled.

The final Group Policy Management inspection confirmed:

- Troy Workstation Policy: Link Enabled = Yes
- Domain Workstation Security Baseline: Link Enabled = Yes
- Enforced = No for both links
- GPO Status = Enabled

No changes to the Settings Page Visibility policy value were required.

### Validation Status

**Resolved — Client-side validation completed October 16, 2026.**

After enabling the Troy Workstation Policy link on the Troy Computers OU, connectivity to the domain controller was restored and Group Policy processing completed.

While signed in as `MASONMFG\test.employee` on `TROY-WIN11-01`:

- `gpresult /r` confirmed that Troy Workstation Policy was applied.
- Windows Settings → System no longer displayed the About page.
- The previously validated Run command restriction continued to demonstrate user-side policy enforcement.

The successful endpoint behavior confirmed that the configured `hide:about` restriction was functioning.

The issue was resolved without modifying the original Settings Page Visibility policy value.

### Lesson Learned

Group Policy troubleshooting must distinguish between user and computer configuration scopes.

A GPO successfully applying user-side restrictions does not guarantee that its computer-side settings are being applied.

Organizational unit placement, GPO link state, policy configuration, and Resultant Set of Policy should be examined before changing existing policy values.



---

## Case 10 — Stale GNS3 Link Disrupting Mason Server Connectivity

### Problem

The Ubuntu Server hosting Kea DHCP experienced a connectivity failure between the GNS3 virtual network and the physical Mason infrastructure.

The failure affected the server's ability to communicate with its default gateway and reach external networks.

### Symptoms

- Ubuntu Server (`10.10.30.20`) could successfully ping Windows Server (`10.10.30.10`).
- Ubuntu could not ping its default gateway (`10.10.30.1`).
- Ubuntu could not reach `8.8.8.8`.
- MASON-R1 could not successfully ping the Ubuntu Server.

### Investigation

Ubuntu's network configuration was inspected. Its IP address, subnet mask, and default route were correct.

On MASON-SW1, the relevant physical interfaces were examined:

- `Fa0/5` — GNS3-side trunk
- `Fa0/24` — Router-side trunk

VLAN 30 was allowed, active, and forwarding on the relevant trunks.

However, the VLAN 30 MAC address table contained the router-side dynamic MAC address on `Fa0/24` but did not show the expected GNS3-side MAC address on `Fa0/5`.

This suggested that the problem was within the Layer 2 path between GNS3 and the physical switching infrastructure rather than Ubuntu's IP configuration.

### Corrective Action

The affected GNS3 virtual connection was disconnected and reconnected.

No changes to Ubuntu's IP addressing or the Cisco VLAN configuration were required.

### Validation

After restoring the GNS3 connection, Ubuntu successfully pinged `10.10.30.1` with 0% packet loss.

This confirmed restoration of connectivity between the Ubuntu Server and its Mason VLAN 30 gateway.

### Findings

The available evidence supports a stale or nonfunctional GNS3 virtual connection as the immediate cause of the connectivity failure.

The specific underlying mechanism responsible for the link becoming nonfunctional was not determined.

Internet connectivity was not independently revalidated as part of this particular restoration test.

### Lesson Learned

Correct IP addressing, active physical interfaces, and valid trunk configurations do not guarantee end-to-end Layer 2 connectivity.

MAC address table inspection can help identify where expected traffic is missing.

Virtual network connections should be verified independently before modifying otherwise valid routing or server configurations.



---

## Case 11 — Mason Workstation DHCP Failure and APIPA Address

### Problem

During the integration of `MASON-WIN11-01` into Mason VLAN 20, the workstation failed to obtain an IPv4 address from the centralized Kea DHCP server.

Windows automatically assigned an APIPA address instead.

### Symptoms

- MASON-WIN11-01 received `169.254.20.237`.
- `ipconfig /renew` timed out.
- The workstation could not obtain a valid lease from Kea DHCP.
- Wireshark captured outbound DHCP Discover packets without corresponding DHCP Offer responses.

### Investigation

Wireshark confirmed that the workstation generated DHCP Discover broadcasts addressed to `255.255.255.255`.

The Mason router's VLAN 20 subinterface was inspected.

MASON-R1 `GigabitEthernet0/0.20` was configured with:

- 802.1Q VLAN encapsulation: `20`
- IP address: `10.10.20.1/24`
- DHCP relay: `ip helper-address 10.10.30.20`

The router subinterface and DHCP relay configuration were verified as correct.

Further investigation showed that the Ubuntu Kea server was not receiving the expected relayed DHCP requests.

The connection between Ubuntu Server and the GNS3 virtual switching infrastructure was examined.

### Root Cause

A stale GNS3 virtual connection disrupted communication between the DHCP server and the network.

This prevented the relayed DHCP requests from reaching the centralized Kea service.

The failure was not caused by an incorrect VLAN 20 addressing scheme, DHCP relay command, or Kea DHCP scope configuration.

The underlying reason for the GNS3 connection becoming nonfunctional was not determined.

### Resolution

The affected GNS3 connection between Ubuntu Server and the virtual network was disconnected and reconnected.

No changes to the router's DHCP relay configuration or Kea DHCP scope were required.

### Validation

After restoring the connection:

- MASON-WIN11-01 successfully obtained a valid Mason VLAN 20 DHCP lease.
- The workstation proceeded with Active Directory domain integration.
- MASON-WIN11-01 successfully joined `masonmfg.internal`.

The exact final DHCP lease address was not preserved in the available validation record.

### Lesson Learned

An APIPA address indicates that Windows could not obtain a valid DHCP lease, but it does not independently identify the source of the failure.

Packet captures, relay configuration verification, and server-side traffic observation helped isolate the problem.

Valid DHCP configuration does not guarantee successful operation when the underlying virtual network connection is disrupted.

Troubleshooting should follow the DHCP traffic path from client to relay to server before making configuration changes.



---

## Case 12 — Mason Windows 11 QEMU/UEFI Boot Failure

### Problem

While creating an independent Windows 11 Pro workstation for the Mason corporate site, the new GNS3 virtual machine repeatedly booted into the UEFI shell instead of Windows.

The goal was to create a separate Mason workstation without modifying or disrupting the existing Troy workstation.

### Symptoms

- The new Mason workstation entered the UEFI shell.
- The initial Mason disk configuration referenced the Troy workstation's base image.
- Changes to the disk overlay did not consistently persist because the node remained associated with the original Troy QEMU template.
- The copied Mason QEMU template initially used an IDE disk interface instead of the SATA/AHCI configuration used by the working Troy workstation.
- An accidental `-cput host` parameter caused a separate QEMU startup error before being corrected to `-cpu host`.

### Investigation

The working Troy workstation was used as a reference to compare QEMU settings.

The investigation included:

- Comparing the Mason and Troy QEMU templates.
- Inspecting QCOW2 images and backing-file relationships using `qemu-img info`.
- Checking disk integrity with `qemu-img check`.
- Examining UEFI firmware configuration and boot files.
- Confirming the Mason disk contained a valid GPT partition table and EFI System Partition.
- Verifying that Windows boot files, including `bootmgfw.efi`, were present.
- Comparing the runtime disk attachment methods used by the Mason and Troy virtual machines.

The Mason base image was confirmed to contain the expected Windows installation and EFI boot structure.

This shifted attention toward the QEMU template and virtual disk attachment configuration rather than a missing Windows installation.

### Root Cause

The Mason virtual machine's QEMU configuration did not match the working Windows installation's required disk attachment setup.

The initial template also incorrectly referenced the Troy base disk.

The decisive boot issue was that Mason launched with an IDE disk configuration rather than the SATA/AHCI configuration used by the working Troy environment.

### Resolution

A separate Mason base disk was created from the verified Troy backup:

`Mason-Win11-Client-hda.qcow2`

The standalone image was validated with `qemu-img check` and `qemu-img info`.

Validation confirmed:

- 64 GiB virtual disk capacity.
- No backing file for the standalone Mason base image.
- No reported QCOW2 corruption.

A dedicated Mason QEMU template was configured with:

- The independent Mason QCOW2 base image.
- SATA disk interface.
- UEFI firmware enabled.
- Corrected `-cpu host` configuration.

The broken Mason node was replaced with a new node using the corrected template.

A fresh QCOW2 overlay was created against the independent Mason base.

The original Troy workstation and its disk were preserved.

### Validation

After correcting the QEMU disk configuration:

- The Mason virtual machine successfully progressed past the UEFI shell.
- Windows Setup booted successfully.
- The workstation subsequently completed Windows setup and generalization.
- `MASON-WIN11-01` was successfully deployed on Mason VLAN 20.
- The workstation joined the `masonmfg.internal` domain.

### Lesson Learned

A virtual disk containing a valid operating system and EFI boot files may still fail to boot when its virtual hardware configuration is incorrect.

Troubleshooting virtual machine boot failures should distinguish disk integrity, firmware configuration, backing-image relationships, and virtual storage controller settings.

Comparing a malfunctioning virtual machine against a known-working configuration can help isolate the actual problem without unnecessarily rebuilding the operating system.



---

## Case 13 — FortiGate and MASON-R1 Transit ARP Failure

### Problem

During subsequent Mason network testing, connectivity between MASON-R1 and the FortiGate virtual firewall failed on the dedicated `10.10.40.0/30` transit network.

This occurred after earlier successful Internet connectivity validation from both the Mason infrastructure and Troy workstation.

### Symptoms

- MASON-R1 could not ping the FortiGate transit address `10.10.40.1`.
- FortiGate could not ping the MASON-R1 transit address `10.10.40.2`.
- MASON-R1 displayed an incomplete ARP entry for `10.10.40.1`.
- Both transit interfaces appeared operational.

### Investigation

The transit interface configurations were inspected.

**MASON-R1:**

- Interface: `GigabitEthernet0/0.40`
- IP address: `10.10.40.2/30`
- Interface status: Up/Up

**FortiGate:**

- Interface: `port3`
- IP address: `10.10.40.1/30`
- Interface status: Up
- Negotiated speed: 1000 Mbps, full duplex

The physical Mason switch configuration was also investigated.

MASON-SW1 showed VLAN 40 MAC addresses associated with:

- `Fa0/23` — FortiGate-side connection
- `Fa0/24` — Router-side connection

The FortiGate-facing `Fa0/23` interface was confirmed as a static access port assigned to VLAN 40 (`FIREWALL-TRANSIT`).

Despite the apparent interface and VLAN connectivity, MASON-R1 could not successfully resolve the FortiGate address through ARP.

### Findings

The incomplete ARP entry indicates that MASON-R1 was not successfully resolving the Layer 2 address associated with `10.10.40.1`.

The available evidence does not establish whether the failure originates from the GNS3 virtual connection, physical/virtual bridging, VLAN handling, or another part of the transit path.

The presence of MAC addresses in the switch table does not independently prove successful end-to-end ARP communication.

### Root Cause

**Not yet determined.**

Although separate stale GNS3 connection problems were previously identified elsewhere in the environment, the FortiGate transit failure has not been proven to have the same underlying cause.

### Resolution Status

**Unresolved — further troubleshooting required.**

No permanent corrective action or successful restoration of transit connectivity has been validated for this incident.

### Planned Validation

Further investigation should proceed incrementally:

1. Confirm the current operational status of the relevant GNS3 links.
2. Recheck the FortiGate and MASON-R1 transit interface configurations.
3. Verify VLAN 40 membership, trunk configuration, and forwarding.
4. Examine ARP traffic across the transit path to identify where requests or responses stop.
5. Make one evidence-supported corrective change at a time.
6. Repeat bidirectional transit connectivity tests before testing external Internet access.

### Lesson Learned

An operational interface and apparently correct IP configuration do not guarantee functioning Layer 2 communication.

ARP inspection helps distinguish address-resolution failures from ordinary Layer 3 routing problems.

Previously successful connectivity tests should be preserved as historical validation, while newly discovered failures must be documented separately.

A suspected cause should not be presented as confirmed until supported by troubleshooting evidence.



## Case 14 — Troy SMB Shared-Folder Access Restriction

### Problem

The Troy Windows 11 workstation encountered an access restriction when attempting to open the Mason Windows Server's CompanyShare resource through direct UNC navigation in File Explorer.

### Symptoms

- The Troy client had working connectivity to the Mason domain controller at `10.10.30.10`.
- TCP port 445 was reachable.
- Direct access to `\\10.10.30.10\CompanyShare` produced an access restriction message.
- Normal File Explorer network browsing did not provide the expected access.

### Investigation

The troubleshooting process distinguished network reachability from file-sharing access.

The Troy client was already joined to `masonmfg.internal` and authenticated as `MASONMFG\test.employee`.

Active Directory security group membership and the server's share configuration were examined during subsequent validation.

The test account belonged to `Shared-Resources-Group`, which had NTFS Modify permissions and SMB Change and Read permissions on CompanyShare.

### Workaround

The shared folder was successfully mapped using PowerShell:

`New-PSDrive -Name Z -PSProvider FileSystem -Root "\\WIN-F40P5E8HDVL\CompanyShare" -Persist`

The mapped drive appeared as `Z:` in File Explorer.

### Validation

- The Troy user successfully accessed the mapped CompanyShare drive.
- The user modified and saved the `Company Information` file.
- The updated file was opened on the Mason Windows Server, confirming the cross-site modification.
- Windows Security Event 4624 separately confirmed successful network authentication by `MASONMFG\test.employee` from `10.20.20.100`.

### Root Cause

The exact cause of the original direct UNC navigation restriction was not determined.

The successful mapped-drive test confirms that SMB connectivity and authorized file modification were operational, but does not establish why the original navigation method was restricted.

### Resolution Status

**SMB file access validated — original UNC navigation restriction unresolved.**

No unsupported root-cause claim is made.

### Lesson Learned

Successful TCP connectivity does not by itself establish application-level access.

When troubleshooting file-sharing problems, distinguish network reachability, domain authentication, share and NTFS permissions, and the method used to access the resource.

A successful alternative access method can validate service functionality without necessarily resolving the original error.






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