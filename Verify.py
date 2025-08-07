
from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from Network.Devices import Routers, vpn_routers, Firewalls, Edge_Routers




# VERIFYING VLANS on ACCESS SWITCHES:
rp('\n[bold cyan]----------Verifying VLANs---------[/bold cyan]')
for devices in Switches.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show vlan brief', use_textfsm=True)
    rp(host,output, sep='\n')



# VERIFYING HSRPv2 and VRRP
rp('\n[bold cyan]----------Verifying HSRPv2 on Edge_Routers and And Core Switches---------[/bold cyan]')    
for devices in chain(Routers.values(),Edge_Routers.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show standby brief')
    rp(host,output, sep='\n')
rp('\n[bold cyan]----------VRRP on Branch Routers---------[/bold cyan]')  
for devices in Spokes.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show vrrp brief')
    rp(host,output, sep='\n')



# VERIFYING OSPF ON CORE ROUTERS:
rp('\n[bold cyan]----------Verifying OSPF on CORE ROUTERS---------[/bold cyan]')
for devices in Routers.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show ip route ospf')
    rp(host,output, sep='\n')



# VERIFYING BGP NLRI ON EDGE ROUTERS:
rp('\n[bold cyan]----------Verifying BGP NLRI on EDGE ROUTERS---------[/bold cyan]')
for devices in Edge_Routers.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show ip bgp')
    rp(host,output, sep='\n')


