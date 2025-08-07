
from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from rich.prompt import Prompt
from jinja2 import FileSystemLoader, Environment
from Network.Devices import uplink_routers, svr_firewalls, Edge_Routers, vpn_routers, edge_firewalls



# Jinja Templates Directory filepath:
Template_dir =input('Jinja Templates Directory filepath: ')


# # Configuring Netflow:
# rp(f'[bold cyan]----------Configuring NetFlow----------[/cyan]')
# for devices in vpn_routers.values():
#     c = ConnectHandler(**devices)
#     c.enable()
#     host  = c.send_command('show version', use_textfsm=True)[0]['hostname']

#     server = input('IP address of the Flow Collector: ')
#     interface = input(f'{host} Netflow source interface: ')
#     Port = input(f'{host} Netflow UDP-Port: ')
#     data = {
#             'Flow_Interface': interface,
#             'UDP_Port': Port,
#             'Server_IP': server  
#            }
#     env = Environment(loader=FileSystemLoader(Template_dir))
#     template = env.get_template('NetFlow.j2')
#     commands = template.render(data)
#     rp(c.send_config_set(commands.splitlines()),'\n')
#     c.save_config()
#     c.disconnect()


# # Configuring NTP
# rp(f'\n[bold cyan]----------Configuring NTP on Network Devices---------[/bold cyan]')
# for devices in chain(Firewalls.values(), Routers.values(), vpn_routers.values(),Edge_Routers.values()):
#     c = ConnectHandler(**devices)
#     c.enable()
#     host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
#     ntp = input(f'NTP server IP for host  {host}: ')
#     source = input(f'{host} NTP source interface: ')
#     data = {
#             'ntp_server': ntp,
#             'source_intf': source
#            }
#     env = Environment(loader=FileSystemLoader(Template_dir))
#     template = env.get_template('NTP.j2')
#     commands = template.render(data)
#     rp(c.send_config_set(commands.splitlines()),'\n')
#     c.save_config()
#     c.disconnect()


#Configuring CoPP
rp(f'\n[bold cyan]----------Configuring Edge Routers---------[/bold cyan]')
for devices in chain(edge_firewalls.values(), svr_firewalls.values(), uplink_routers.values(),vpn_routers.values(),Edge_Routers.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    eigrp_enabled = input(f'Is EIGRP protocol Running on {host} (Y/N): ')
    ospf_enabled = input(f'Is OSPF protocol Running on {host} (Y/N): ')
    data = {
            'eigrp_enabled': eigrp_enabled,
            'ospf_enabled': ospf_enabled
           }
    env = Environment(loader=FileSystemLoader(Template_dir))
    template = env.get_template('CoPP.j2')
    commands = template.render(data)
    rp(c.send_config_set(commands.splitlines()),'\n')
    c.save_config()
    c.disconnect()


# Configure Syslog
rp(f'\n[bold cyan]----------Configuring Syslog---------[/bold cyan]')
for devices in chain(uplink_routers.values(), vpn_routers.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']

    commands = ['logging host 172.19.18.150',
                'logging monitor informational']
    output = c.send_config_set(commands)
    rp(host,output, sep='\n')
    c.save_config()
    c.disconnect()


# # COnfigure banner MOTD
# rp('[cyan]----------Configuring MOTD banner---------[/cyan]')
# for devices in chain(uplink_routers.values(), vpn_routers.values(),edge_firewalls.values(), svr_firewalls.values(),Edge_Routers.values()):
#     c = ConnectHandler(**devices)
#     c.enable()
#     host = c.send_command('show version',use_textfsm=True)[0]['hostname']
#     commands = [
#                 'banner login @',
#                f'{"*"*50}',
#                f'{" "*13}{host}',
#                f'{" "*7}RMS MEDIA COMPANY LIMITED',
#                f'{" "}Unauthorized access is strictly forbidden',
#                f'{"*"*50}',
#                '@']
#     rp(c.send_config_set(commands),'\n')
#     c.save_config()
#     c.disconnect()


# # Configure EEM
# rp(f'\n[bold cyan]----------Configuring Embedded Event Manager--------[/bold cyan]')
# Server_IP = Prompt.ask("[bright_magenta]IP address of the TFTP server: [/]")
# for devices in chain(Routers.values(), Firewalls.values(),Edge_Routers.values(),vpn_routers.values()):
#     c = ConnectHandler(**devices)
#     c.enable()
#     host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
#     Config_filename = Prompt.ask(f'[magenta]Name of the configuration file for host {host} (with .txt extension): [/]')
#     data = {
#             'Server_IP': Server_IP,
#             'Config_filename': Config_filename
#            }
#     env = Environment(loader=FileSystemLoader(Template_dir))
#     template = env.get_template('EEM.j2')
#     commands = template.render(data)
#     rp(c.send_config_set(commands.splitlines()),'\n')
#     c.save_config()
#     c.disconnect()

