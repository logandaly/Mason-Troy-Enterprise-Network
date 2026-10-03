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

