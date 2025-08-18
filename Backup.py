
from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from rich.prompt import Prompt
from Network.Devices import vpn_routers, svr_firewalls, edge_firewalls, Edge_Routers, uplink_routers, Access_switches, Svr_switches, Core_Switches, Border_switches
from csv import writer
import yaml



# RUNNING CONFIGS
rp('[bold cyan]----------Backing Up configurations---------[/bold cyan]')
filepath = Prompt.ask('[bright_magenta]Running-configs filepath [/]')
for devices in chain(vpn_routers.values(), uplink_routers.values(), 
                     Edge_Routers.values(), svr_firewalls.values(),edge_firewalls.values(),
                     Svr_switches.values(),Border_switches.values(),Access_switches.values(),Core_Switches.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host   = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show run')

    with open(f'{filepath}/{host}', 'w')as f:
        f.write(output)
    rp(f'The running configuration of {host} has been backed up!!')



# DEVICES' INVENTORY
rp('\n[bold cyan]----------Device Inventory----------[/bold cyan]')
filepath = Prompt.ask('[bright_magenta]Inventory filepath [/]')
with open (f'{filepath}/Data.csv', 'w')as f:
    write_data = writer(f)
    write_data.writerow(['Hostname','IP address','Software Image','Version','Serial number'])
    for devices in chain(vpn_routers.values(), uplink_routers.values(), 
                     Edge_Routers.values(), svr_firewalls.values(),edge_firewalls.values(),Svr_switches.values(),
                     Border_switches.values(),Access_switches.values(),Core_Switches.values()):
        c = ConnectHandler(**devices)
        c.enable()
        output = c.send_command('show version',use_textfsm=True)[0]

        hostname = output['hostname']
        ip_addr  = devices['ip']
        image    = output['software_image']
        version  = output['version']
        serial   = output['serial']

        write_data.writerow([hostname,ip_addr,image,version,serial])
        rp(f'Finished taking {hostname} Inventory')
        c.disconnect()


# for devices in chain(vpn_routers.values(), uplink_routers.values(), 
#                      Edge_Routers.values(), svr_firewalls.values(),edge_firewalls.values(),Svr_switches.values(),
#                      Border_switches.values(),Access_switches.values(),Core_Switches.values()):
#     c = ConnectHandler(**devices)
#     c.enable()
#     output = c.send_command('show version',use_textfsm=True)[0]

#     # yaml_output = yaml.dump(output,indent=4)
    
#     # rp(output["hostname"],'\n',yaml_output)
#     rp(output["hostname"],'\n',output)
#     c.disconnect()