\# Wireless Network Assessment — Mason–Troy Enterprise Network



\## 1. Purpose and Scope



This assessment evaluates the requirements for a potential wireless network expansion at the Mason and Troy facilities.



The implemented capstone network uses wired Cisco infrastructure and GNS3 virtual endpoints. Wireless access points and wireless clients were not deployed or tested.



The following assessment is a proposed design based on illustrative enterprise requirements rather than measured wireless survey data.



\## 2. Wireless Client Capacity



For initial planning, the organization is assumed to require support for approximately 30–50 wireless devices across both facilities.



Potential wireless clients include:



\- Employee laptops and mobile devices

\- Authorized administrative devices

\- Guest devices, where permitted

\- Future wireless business equipment



Device counts should be confirmed through an inventory and an assessment of peak simultaneous usage before deployment.



\## 3. Bandwidth Assessment



Wireless bandwidth requirements depend on the number of simultaneous clients and their applications.



A preliminary planning scenario assumes 40 concurrent clients, each requiring an average of 5 Mbps during a busy period.



\*\*Estimated application demand:\*\*



40 clients × 5 Mbps = 200 Mbps



This is an illustrative aggregate workload, not a measured throughput requirement.



Additional capacity would be needed for wireless overhead, application bursts, retransmissions, and future growth.



The design should consider access-point capabilities, wired uplink speeds, switch capacity, and the available Internet connection.



A 1 Gbps wired access-point uplink would be a reasonable starting point for evaluation, subject to actual hardware capabilities and measured traffic.



\## 4. Proposed Access Point Placement



Access points should be positioned to provide adequate coverage and distribute users across available radio capacity.



\*\*Mason facility\*\*



Initial planning could evaluate two access points:



\- One serving the primary employee workspace

\- One serving another high-demand office or shared working area



\*\*Troy facility\*\*



Initial planning could evaluate one or two access points:



\- One serving the primary employee workspace

\- An additional access point if the floor plan, building materials, or client density require it



These quantities are preliminary assumptions only.



Final placement should be determined through an RF site survey that considers floor plans, wall materials, interference, channel overlap, and signal coverage.



\## 5. Network Integration and Segmentation



Wireless connectivity should integrate with the existing Mason–Troy enterprise architecture.



Proposed considerations include:



\- Assigning corporate wireless clients to authorized employee networks or dedicated wireless VLANs.

\- Keeping wireless guests isolated from Active Directory, management systems, and server infrastructure.

\- Using controlled routing and firewall policies between wireless networks and protected resources.

\- Preserving the isolation of Troy's Legacy/OT VLAN 30.

\- Providing centralized DHCP and DNS services where appropriate.



Any additional wireless VLANs would require updates to the IP addressing plan, DHCP scopes, switch trunks, routing, and security policies.



\## 6. Wireless Security



The proposed deployment should use modern enterprise wireless security controls.



Recommended measures include:



\- WPA3-Enterprise where supported by clients and access points.

\- IEEE 802.1X authentication using a centrally managed RADIUS service.

\- Separate corporate and guest wireless access.

\- Appropriate firewall and ACL restrictions.

\- Protected access-point management interfaces.

\- Regular firmware updates and configuration backups.

\- Wireless monitoring and logging.



Legacy wireless devices should be assessed individually. Insecure compatibility requirements should not weaken the enterprise wireless network.



\## 7. Performance and Coverage Validation Plan



If wireless is implemented in a later project phase, validation should include:



1\. A wireless coverage and channel-interference survey.

2\. Concurrent client association and authentication testing.

3\. DHCP and DNS functionality.

4\. Internal network and Internet reachability.

5\. Throughput and latency testing under realistic load.

6\. Roaming performance between access points.

7\. Guest and corporate VLAN isolation.

8\. Wireless security and access-control testing.



No wireless performance measurements were conducted during this capstone.



\## 8. Assessment Conclusion



A future wireless deployment appears feasible as an extension of the existing routed and segmented Mason–Troy network, subject to facility surveys, hardware selection, uplink-capacity checks, and security validation.



\*\*Assessment Status: PROPOSED DESIGN — Not Implemented\*\*



This assessment addresses wireless client capacity, bandwidth planning, access-point placement, and security considerations without representing hypothetical results as completed deployment evidence.
