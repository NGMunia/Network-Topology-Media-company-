
from login import Username, Password, Secret


vpn_routers  =  {
            'Hub': { 
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.0.1'
                    },
          'TX_ST_1':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.0.4'
                    },
          'TX_ST_2':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.0.5'
                    },
         'BR_RTR_1':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.0.2'
                    },
         'BR_RTR_2':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.0.3'
                    } }

uplink_routers =   {
         'STR_RTR': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.0.0.10'
                    },
      'Uplink_RTR': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.19.1'
                    } }

svr_firewalls =   {
        'SVR_FW_1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.18.1',
                   },
        'SVR_FW_2':  {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.18.2'
                   } }

edge_firewalls = {
       'BDR_FW_1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'2001:32:19:86::253'
                   },
       'BDR_FW_2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'2001:32:19:86::254'
                   } }

Edge_Routers = {
          'Edge-1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'2001:32:19:86::1',
                    },
          'Edge-2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'2001:32:19:86::2'
                    } }

Switches= {
           'CORE_1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.16.1'
                      },
          'CORE_2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.116.1'
                    },
        'SW-BLD-1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.16.10'
                    },
        'SW-BLD-2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.16.11'
                    },
        'SW-BLD-3': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.16.12'
                    },
          'SW-BR2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.1.20.10'
                    },
          'SW-SVR': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.19.18.10'
                    },
        'SW1-Edge': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'2001:32:19:86::10'
                    },
        'SW2-Edge': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'2001:32:19:86::11'
                    } }
