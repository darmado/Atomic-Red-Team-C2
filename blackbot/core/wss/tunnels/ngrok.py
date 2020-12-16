import re
import os
import requests
import subprocess
from time import sleep
from blackbot.core.utils import get_path_in_package

class ARTIC2Tunnel:
    def __init__(self):
        self.name = 'ngrok'

    def status(self):
        try:
            req = requests.get('http://localhost:4040/api/tunnels')
            return True
        except:
            return False

    def kill_ngrok(self):
        subprocess.run(['killall ngrok'], stdout=subprocess.PIPE, shell=True)

    def connect(self, target):
        if target.lower() == 'kill':
            if self.status():
                self.kill_ngrok()
                out = 'Ngrok killed'
                return out

            else:
                out = 'Ngrok is not running'
                return out

        else:
            if self.status():
                out = 'Ngrok is already running'
                return out
            
            else:
                log_path = '/opt/artic2/blackbot/core/wss/tunnels/'
                
                subprocess.run([f'ngrok http 80 -log=stdout > {log_path}ngrok.log &'], stdout=subprocess.PIPE, shell=True)
                sleep(2)
                with open(os.path.join(log_path, 'ngrok.log')) as log:
                    info = log.read()
                    tunnel_http = re.findall('url=http://.{21}', info)
                    tunnel_https = re.findall('url=https://.{21}', info)
                    print(tunnel_http[0])
                    print(tunnel_https[0])

                urls = [tunnel_http[0], tunnel_https[0]]
                out = 'URLs to download stager\n'
                for url in urls:
                    out += f'{url}/{target}\n'
                return out

