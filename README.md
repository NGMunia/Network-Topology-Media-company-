
# Network-Topology (media Company)



![VPNs](https://img.shields.io/badge/VPNs-DMVPN%20%7C%20IPSec-blue)
![Switching](https://img.shields.io/badge/Switching-LACP%20%7C%20VLANs-Red)
![Assurance](https://img.shields.io/badge/Assurance-SNMP%20%7C%20Syslog%20%7C%20SPAN-Red)
![Automation](https://img.shields.io/badge/Automation-Python-orange)
![Routing](https://img.shields.io/badge/Routing-EIGRP%20%7C%20OSPF%20%7C%20BGP%20%7C%20Multicast-Red)
![Security](https://img.shields.io/badge/Security-CoPP%20%7C%20ZBF-blue)
![Dualstack](https://img.shields.io/badge/Dualstack-IPv4%20%7C%20IPv6-blue)

---

## summary of the network:


The topology demonstrates a **Dual stack (IPv4 and IPv6)** network topology with a collapsed core while employing software-defined networking (Automation).

All remote sites are linked with a single-hub DMVPN for site-to-site VPN connectivity, with IPv6 as the transport network and IPv4 as the overlay network. 

The network is also configured as BGP-AS-5689 as a non-transit Network.

Internet connectivity is through IPv6 while internal and remote site connectivity is IPv4 only.


![Topology](/Network/Topology.png)


---
## At a glance:

**Design Highlights**

- Dual‑stack architecture (IPv4 overlay / IPv6 transport)

- Collapsed core design for scalability and simplicity

- DMVPN Phase 2 for secure site‑to‑site connectivity

- Multi‑protocol routing (OSPFv3, EIGRP, BGP)

- Policy‑driven security (ZBF, CoPP)

- Network automation using Python, Ansible, and Jinja2

- Full monitoring, QoS, and traffic analysis


**Technologies Used**

- Routing: OSPFv3, EIGRP (Named), BGP, Multicast (PIM‑SM)

- Switching: VLANs, LACP (EtherChannel)

- VPN: DMVPN Phase 2 over IPSec

- Security: Zone‑Based Firewall, CoPP

- Automation: Ansible, Python (Netmiko), Jinja2, EEM

- Monitoring: SNMP, Syslog, NetFlow, SPAN/RSPAN

---
## Layer 2 connectivity:
The network Employs various layer 2 protocols namely:


**LACP**:

The core switch and Access switches are configured with LACP in active-active mode.
Verification is seen below on the ACC-SW1:


``` bash
ACCESS-SWITCH-1#sh etherchannel summary
! Output omitted for brevity
Number of channel-groups in use: 2
Number of aggregators:           2

Group  Port-channel  Protocol    Ports
------+-------------+-----------+------------------------
1      Po1(SU)         LACP      Et1/0(P)    Et1/1(P)
2      Po2(SU)         LACP      Et1/2(P)    Et1/3(P)

```
---

## Layer 3 connectivity:
The network Employs various layer 3 protocols namely:


**InterVLAN Routing**:


The network topology is designed as a collapsed core, where the core switches assume the responsibilities of both the core and distribution layers. 

InterVLAN routing is configured, enabling communication between different VLANs within the network.


**Multi-Area OSPFv3**:

In the HQ region, OSPFv3 (both IPv4 and IPv6) is implemented to manage and optimize the routing infrastructure. 

The network is built using an inter-area OSPF architecture, which helps improve scalability and manageability by dividing the infrastructure into areas.

This design promotes a modular and well-organized structure.

Within the HQ region, each area functions independently, leading to better overall performance, lower routing overhead, and more controlled propagation of LSAs.



```bash
Sample config
CORE_SWITCH#sh ip route ospfv3

Gateway of last resort is not set

      172.19.0.0/16 is variably subnetted, 6 subnets, 2 masks
O IA     172.19.18.0/24 [110/10010] via 10.19.18.6, 01:10:54, Ethernet2/2
                        [110/10010] via 10.19.18.2, 01:10:54, Ethernet2/1
O IA     172.19.19.0/25 [110/30000] via 10.0.0.10, 01:10:49, Ethernet3/1
O IA     172.19.19.128/25 [110/20000] via 10.0.0.10, 01:10:49, Ethernet3/1
O E2     172.19.111.0/24 [110/20] via 10.0.0.14, 01:09:59, Ethernet2/3
O E2     172.19.112.0/24 [110/20] via 10.0.0.14, 01:09:59, Ethernet2/3
O E2     172.19.116.0/24 [110/20] via 10.0.0.14, 01:09:59, Ethernet2/3
      172.20.0.0/24 is subnetted, 2 subnets
O E2     172.20.1.0 [110/20] via 10.0.0.14, 01:09:58, Ethernet2/3
O E2     172.20.2.0 [110/20] via 10.0.0.14, 01:09:31, Ethernet2/3
O E2  192.168.0.0/24 [110/20] via 10.0.0.14, 01:04:58, Ethernet2/3
CORE_SWITCH#
CORE_SWITCH#
CORE_SWITCH#sh ipv6 route ospf
IPv6 Routing Table - default - 4 entries
OE2 ::/0 [110/1], tag 1
     via FE80::253, Ethernet3/2
     via FE80::254, Ethernet3/3
OI  2001:32:19:18::/64 [110/10010]
     via FE80::18, Ethernet2/2
     via FE80::18, Ethernet2/1
OI  2001:32:19:86::/64 [110/20000]
     via FE80::253, Ethernet3/2
     via FE80::254, Ethernet3/3
CORE_SWITCH#
```

**EIGRP**:

Within the network infrastructure, EIGRP (Named mode) is used in routing within mGRE tunnels, specifically configured under DMVPN architecture.

To enhance the efficiency of the network, spokes within the mGRE tunnels are optimized as stub routers. 

This minimizes the likelihood of Stuck-in-Active scenarios.

Bandwidth optimization feature is employed to limit EIGRP bandwidth usage.


```bash
Sample config:

TX-STN-1#sh running-config | s r e
router eigrp EIGRP
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface Tunnel0
   bandwidth-percent 25
  exit-af-interface
  !
  af-interface Ethernet0/0
   passive-interface
  exit-af-interface
  !
  topology base
  exit-af-topology
  network 172.20.1.0 0.0.0.255
  network 192.168.0.0
  eigrp stub connected summary
 exit-address-family

```

**Multicast  PIM-sparse-mode**

The media server is used to send multicast traffic from studio to main uplink station.

The stream_RTR acts as RP.

To verify Multicast routing:

```bash
STREAM_MEDIA_ROUTER#ping 239.1.1.10
Type escape sequence to abort.
Sending 1, 100-byte ICMP Echos to 239.1.1.10, timeout is 2 seconds:

Reply to request 0 from 172.19.19.1, 1 ms
```

The multicast routing table can be verified on the Hub router:
```bash
STREAM_MEDIA_ROUTER#sh ip mroute
 
(*, 239.1.1.10), 01:16:58/00:03:17, RP 10.0.0.13, flags: SF
  Incoming interface: Null, RPF nbr 0.0.0.0
  Outgoing interface list:
    Ethernet0/2, Forward/Sparse, 01:16:58/00:03:17

(172.19.19.129, 239.1.1.10), 00:00:48/00:02:46, flags: FT
  Incoming interface: Ethernet0/1, RPF nbr 0.0.0.0
  Outgoing interface list:
    Ethernet0/2, Forward/Sparse, 00:00:48/00:03:17

(10.0.0.13, 239.1.1.10), 00:00:48/00:02:16, flags: PT
  Incoming interface: Ethernet0/2, RPF nbr 0.0.0.0
  Outgoing interface list: Null

```


**BGP and Asymetric Load bancing**:

BGP peering is formed between EDGE routers and their connected ISPs for both IPv4 and IPv6.
Within the HQ's network architecture, BGP is implemented with a focus as a non-transit site. 
In a non-transit scenario, the network primarily manages its own routes and communicates with external networks, but does not forward traffic on behalf of third-party networks.

This reduces the size of the BGP routing table.


Egress traffic is directed to exit through the Edge-1 router, by configuring two Default IPv6 routes on the edge firewalls,one in conjuction with IPSLA (object tracking) and the other with a higher AD

Ingress traffic is routed through Edge-2 by applying AS-prepending to  32.19.86.0/24 prefix on Edge-1 outbound, influencing the inbound traffic flow through Edge-2 as a better path.


```bash
router bgp 5689
 bgp log-neighbor-changes
 neighbor 2001:4:6:2::1 remote-as 100
 neighbor 44.67.27.5 remote-as 100
 !
 address-family ipv4
  network 32.19.86.0 mask 255.255.255.0
  no neighbor 2001:4:6:2::1 activate
  neighbor 44.67.27.5 activate
  neighbor 44.67.27.5 route-map AS-PREPENDING-MAP out
 exit-address-family
 !
 address-family ipv6
  network 2001:32:19:86::/64
  aggregate-address 2001:32:19::/48 summary-only
  neighbor 2001:4:6:2::1 activate
  neighbor 2001:4:6:2::1 route-map AS-PREPENDING-MAP out
 exit-address-family

ip as-path access-list 10 permit ^$
!
route-map AS-PREPENDING-MAP permit 10
 match as-path 10
 set as-path prepend 5689 5689

 ```

**Redistribution**:

OSPFv3 redistribution: Redistributes EIGRP spoke LAN IPv4 prefixes into the OSPF domain.
EIGRP redistribution: Redistributes Area 18 and 19 IPv4 prefixes into EIGRP.
DMVPN-ROUTER is responsible for redistribution between OSPF and EIGRP domain.
The EIGRP Add-path feature enables redundant prefix advertisement for prefixes in Regional offices.

---

## Automating the Network:
The SDN controller is hosted on an Ubuntu server, serving as a centralized platform for orchestrating network configurations. 
Its primary function is to manage and automate network tasks through Python scripts and Ansible playbooks.


**Automating using Ansible playbook**

The controller uses ansible YML files to automate the network with SSH acting as the southbound controller.
Here's a sample OSPF verification playbook:

```bash
---
- name: OSPF PROTOCOL INFORMATION
  hosts: dmvpn_hub
  gather_facts: no
  tasks:
   - name: "gathering OSPFv3 information..."
     cisco.ios.ios_facts:
       gather_network_resources:
         - ospfv3

   - name: "print gathered ospfv3 information"
     debug:
        msg:
          - hostname: "{{ansible_facts.net_hostname}}"
          - OSPF: "{{ansible_facts.network_resources}}"

 ```

**Automation using Python:**

Python uses Netmiko library.
Netmiko relies on SSH as its Southbound Interface for communication with network devices. 

```bash
# Update the package list
sudo apt-get update

# Upgrade installed packages
sudo apt-get upgrade

# Install pip for Python 3
sudo apt-get install python3-pip

# Install netmiko using pip
pip install netmiko

# Install Jinja2
pip install jinja2
```

Sample code snippet of getting Network device **running configuration** using Netmiko library:

```python
'Router':{
         'device_type':'cisco_ios',
         'username': Username,
         'secret': Secret,
         'password': Password,
         'ip':'10.1.10.1'
         }
c = ConnectHandler(**Router)
c.enable()
print(c.send_command('show run'))

```

#### JINJA2


Jinja2 is a templating engine that allows you to create dynamic templates with placeholders for variables.

When combined with network automation tools like Netmiko Jinja2 helps streamline the configuration process for multiple devices.

First, you'll create a Jinja2 template that contains placeholders for the variables you want to use.

To define a variable in a Jinja2 template, you use the **{{ }} syntax**.

Example: 
```bash
#Intf_template:
  interface {{Interface_name}} 
  Description {{Description}} 
  ip address {{Address}} {{Netmask}} 
  no shut
```

**Parsing Data to the Template**

When rendering a Jinja2 template, you provide a dictionary or an object containing the data you want to use for variable substitution.
The keys in the dictionary correspond to the variable names in the template.

Example:
```python
data = {
        'interface':'e0/1',
        'Description':'Connected to Core-SW-1',
        'ip address':'192.168.1.1 255.255.255.0'
       }
```
During template rendering, Jinja2 replaces the variables in the template with their corresponding values from the data dictionary.
The Environment class in Jinja2 manages the template configurations, including:
  * **_templates loading_**: It knows where to find your templates (templates directory)
 * **_FileSystemLoader_** is a template loader in Jinja2 that loads templates from the file system. It searches for templates in a specified directory on the file system and loads them when requested.
  * **_templates rendering_**: It knows how to take your templates and replace the placeholders with the actual values you provide in the data dictionary
 
```python
#Template Loading:
template_dir = input('Input directory path:')
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(intf_template.j2)

#Template Rendering:
commands = template.render(data.splitlines())
```

With this now you can integrete with NetMiko to configure a device.

```python
from jinja2 import Environment, FileSystemLoader
from netmiko import ConnectHandler

c = ConnectHandler(**Router)
c.enable()

#data
data = {
        'interface':'e0/1',
        'Description':'Connected to Core-SW-1',
        'ip address':'192.168.1.1 255.255.255.0'
       }
template_dir = input('Input directory path:')

# Find the template directory and load the template "intf_template"
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template(intf_template.j2)

# Takes the template and replaces the placeholders with the actual data in the "data" dictionary
commands = template.render(data)

# send and print the commands to the Router using ConnectHandler
print(c.send_config_set(commands))
```

**Automating Backup using EEM**

Embedded event manager can be used to automate network devices' tasks.
In this case, EEM is used to automate backup of start-up configs on a scheduled basis; every Mon to Sat
at 1430hrs.

```bash
event manager environment tftpserver tftp://192.168.12.100/
event manager environment filename SW_BR_2.txt
event manager applet Automatic_Backup_Config
 event timer cron cron-entry "30 14 * * 1-6"
 action 1.0 cli command "enable"
 action 1.1 cli command "debug event manager action cli"
 action 1.2 cli command "conf t"
 action 1.3 cli command "file prompt quiet"
 action 1.4 cli command "do copy start $tftpserver$filename"
 action 1.5 cli command "no file prompt quiet"
 action 1.6 syslog priority informational msg "TFTP backup successful"
```
---

## VPN Services:
DMVPN phase 2 with IPsec is used to secure communications between the HQ and the Branch spokes.
EIGRP is the protocol of choice for routing through the mGRE tunnel.

IPv6 is used as the transport network, while IPv4 is used as the overlay.

```bash
DMVPN_HUB_ROUTER#sh crypto isakmp sa
IPv4 Crypto ISAKMP SA
dst             src             state          conn-id status

IPv6 Crypto ISAKMP SA

 dst: 2001:32:19:86::252
 src: 2001:44:68:1::A
 state: QM_IDLE         conn-id:   1001 status: ACTIVE

 dst: 2001:32:19:86::252
 src: 2001:72:74:1::B
 state: QM_IDLE         conn-id:   1003 status: ACTIVE

 dst: 2001:32:19:86::252
 src: 2001:44:68:1::D
 state: QM_IDLE         conn-id:   1002 status: ACTIVE

 dst: 2001:32:19:86::252
 src: 2001:72:74:1::D
 state: QM_IDLE         conn-id:   1004 status: ACTIVE

```
---
## Network Security:

**Zone-Based Firewalls**

Zone-based firewall services are configured on the Edge-Firewalls (FW-EDGE) with stateful traffic inspection from Inside(Private network) to the Internet.
This is done so that even though the whole IPv6 address block **2001:32:19::48** is advertised only 
**2001:32:19:86::/64** is allowed from the Internet.
The rest of the prefixes (used in LAN arent accessible)


On the Network Mangement block Only DHCP, SYSLOG, DNS, NefFlow and MGT VLAN (172.19.16.0/24)traffic is allowed from outside-in
The monitoring server is configured with 172.19.18.150 while DHCP server is 172.19.18.200

```bash
FW-MANAGEMENT-ZONE#sh policy-map type inspect zone-pair Outside-Inside-zone
policy exists on zp Outside-Inside-zone
  Zone-pair: Outside-Inside-zone

  Service-policy inspect : Outside-Inside-policy

    Class-map: Outside-Inside-class (match-all)
      Match: access-group name Outside-Inside-acl

   Inspect
        Packet inspection statistics [process switch:fast switch]
        udp packets: [24:0]

        Session creations since subsystem startup or last reset 14
        Current session counts (estab/half-open/terminating) [0:0:0]
        Maxever session counts (estab/half-open/terminating) [4:4:0]
        Last session created 00:16:12
        Last statistic reset never
        Last session creation rate 0
        Maxever session creation rate 6
        Last half-open session total 0
        TCP reassembly statistics
        received 0 packets out-of-order; dropped 0
        peak memory usage 0 KB; current usage: 0 KB
        peak queue length 0

FW-MANAGEMENT-ZONE#sh ip access-lists Outside-Inside-acl
Extended IP access list Outside-Inside-acl
    10 permit udp any host 172.19.18.150 eq snmptrap (14 matches)
    20 permit udp any host 172.19.18.150 eq syslog
    30 permit udp any host 172.19.18.50 eq bootps
    40 permit ip 172.19.16.0 0.0.0.255 172.19.18.0 0.0.0.255
    50 permit udp any host 172.19.18.150 eq domain
```

**Control plane Policing (CoPP)**

CoPP is a security feature that protects the control plane of a router from unnecessary or Denial-of-Service (DoS) traffic. 
It ensures routing stability, reachability, and packet delivery by providing filtering and rate-limiting capabilities for the control plane packets.

CoPP utilizes the MQC model similar to QOS in its implementation.
It allows for the classification, marking, and policing of traffic based on various criteria.
In the context of CoPP, the MQC model is used to define policies that control the traffic directed towards the control plane of the router or switch

Control plane traffic may be but not limited to Routing protcols, ICMP traffic, NAT, IPSec

In this topology, COPP is configured on core (OSPF, ICMP, SSH traffic) and Edge routers (BGP, ICMP and SSH traffic).

```bash
EDGE-ROUTER-1#sh policy-map control-plane
 Control Plane

  Service-policy input: CoPP-policy

    Class-map: ICMP-traffic-class (match-all)
      170 packets, 19260 bytes
      5 minute offered rate 2000 bps, drop rate 0000 bps
      Match: access-group name ICMP-traffic
      police:
          cir 8000 bps, bc 1500 bytes
        conformed 159 packets, 17962 bytes; actions:
          transmit
        exceeded 11 packets, 1298 bytes; actions:
          drop
        conformed 2000 bps, exceeded 0000 bps

    Class-map: Routing-Protocol-class (match-all)
      14 packets, 1017 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: access-group name Routing-Protocol-acl
      police:
          cir 128000 bps, bc 4000 bytes, be 4000 bytes
        conformed 14 packets, 1017 bytes; actions:
          transmit
        exceeded 0 packets, 0 bytes; actions:
          transmit
        violated 0 packets, 0 bytes; actions:
          transmit
        conformed 0000 bps, exceeded 0000 bps, violated 0000 bps
```

---
# Quality of Service
Scavenger traffic (torrents and leisure streaming platforms) is dropped.
Social media traffic is policed to 512Kbps.

```bash
BRANCH-A-ROUTER-1#sh policy-map interface e0/0.10
 Ethernet0/0.10 
  Service-policy input: Internet-Policy

    Class-map: Scavenger-class (match-any)  
      77 packets, 31359 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: protocol netflix
        77 packets, 31359 bytes
        5 minute rate 0 bps
      Match: protocol bittorrent
        0 packets, 0 bytes
        5 minute rate 0 bps
      drop
    Class-map: Social-media-class (match-any)  
      1936 packets, 160233 bytes
      5 minute offered rate 0000 bps, drop rate 0000 bps
      Match: protocol facebook
        0 packets, 0 bytes
        5 minute rate 0 bps
      Match: protocol twitter
        1936 packets, 160233 bytes
        5 minute rate 0 bps
      Match: protocol instagram
        0 packets, 0 bytes
        5 minute rate 0 bps
      police:
          cir 512000 bps, bc 16000 bytes
        conformed 1936 packets, 160233 bytes; actions:
          transmit 
        exceeded 0 packets, 0 bytes; actions:
          drop 
        conformed 0000 bps, exceeded 0000 bps
```

---
## Network Monitoring
All Routers, Switches  are configured to send SNMP traps to the MGT server.
The MGT server uses PRTG to solicit information via SNMP for general network monitoring, NetFlow for traffic analysis, and Syslog for the capture and analysis of system log data.

On ISP-SW1 and ISP-SW2, we've set up RSPAN to capture VPN traffic and SPAN to capture internet-bound traffic. 
These configurations help monitor and secure the network. The captured data is sent to an Intrusion Detection System (IDS) for analysis. 
This approach enhances our ability to detect and address potential security issues in both VPN and internet traffic.
```bash
Sample RSPAN and SPAN config:
ISP-SWITCH-2#sh monitor session all
Session 1
---------
Type                     : Remote Destination Session
Source RSPAN VLAN      : 87
Destination Ports      : Et3/2
    Encapsulation      : Native


Session 2
---------
Type                     : Local Session
Source Ports             :
    Both                 : Et0/0
Destination Ports      : Et3/3
    Encapsulation      : Native

Sample SNMP config:
  snmp-server community device_snmp RO SNMP-SERVER
  snmp-server system-shutdown
  snmp-server enable traps config
  snmp-server host 172.19.18.150 version 2c device_snmp
```

---

## GNS3 Images used:
* Routers and IOS firewalls: [i86bi_LinuxL3-AdvEnterpriseK9-M2_157_3_May_2018.bin](https://www.gns3.com/marketplace/appliances/cisco-iou-l3)
* Switches: i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin
* SDN conroller: [Ubuntu VM](https://ubuntu.com/desktop)
* IDS: [Ostinato Wireshark](https://gns3.com/marketplace/appliances/ostinato-wireshark)
* UserPC: Windows 7 ISO VM
* End-user PCs: [Webterm Docker](https://gns3.com/marketplace/appliances/webterm)
