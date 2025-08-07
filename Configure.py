
from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from rich.prompt import Prompt
from jinja2 import FileSystemLoader, Environment
from Network.Devices import uplink_routers, svr_firewalls, Edge_Routers, vpn_routers, edge_firewalls



# Jinja Templates Directory filepath:
Template_dir =input('Jinja Templates Directory filepath: ')



#Configuring CoPP ON BORDER ROUTERS AND STREAM ROUTERS
rp(f'\n[bold cyan]----------Configuring COPP on Border and Uplink routers---------[/bold cyan]')
for devices in chain(uplink_routers.values(),Edge_Routers.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    eigrp_enabled = input(f'Is EIGRP protocol Running on {host} (Y/N): ')
    ospf_enabled  = input(f'Is OSPFv3 protocol Running on {host} (Y/N): ')
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



# Configure banner MOTD
rp('[cyan]----------Configuring MOTD banner---------[/cyan]')
for devices in chain(uplink_routers.values(), vpn_routers.values(),edge_firewalls.values(), 
                     svr_firewalls.values(),Edge_Routers.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    commands = [
                'banner login @',
               f'{"*"*50}',
               f'{" "*13}{host}',
               f'{" "*7}RMS MEDIA COMPANY LIMITED',
               f'{" "}Unauthorized access is strictly forbidden',
               f'{"*"*50}',
               '@']
    rp(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()
