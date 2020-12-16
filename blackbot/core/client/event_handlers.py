import logging
from blackbot.core.utils import print_bad, print_good, print_info
from base64 import b64decode
import asyncio

class Witness:
    def __init__(self, option=False):
        self.status = option

    def setStatus(self, option):
        if option == "on":
            self.status = True
        elif option == "off":
            self.status = False
        else:
            logging.warning(f'Usage: Invalid option.')

witness = Witness()

class ClientEventHandlers:
    def __init__(self, connection):
        self.connection = connection

    def stats_update(self, data):
        self.connection.stats.LISTENERS = data['listeners']
        self.connection.stats.SESSIONS = data['sessions']
        self.connection.stats.USERS = data['users']
        self.connection.stats.IPS = data['ips']

    def loadables_update(self, data):
        for ctx, loadables in data.items():
            for lctx in self.connection.contexts:
                if lctx.name == ctx:
                    lctx.available = loadables
    
    def user_login(self, data):
        print_info(f"[{self.connection.alias}] {data}")
    
    def session_staged(self, data):
        print_info(f"[{self.connection.alias}] {data}")

    def new_session(self, data):
        print_info(f"[{self.connection.alias}] {data}")

    def job_result(self, data):
        print_info(f"[{self.connection.alias}] {data['session']} returned job result (id: {data['id']})")
        if witness.status:
            try:    
                x = b64decode(data['output'].encode()).decode()
                aux = x.split("\\r\\n")
                text = ""
                for line in aux:
                    text += line + "\n"

                print(text)
            except:
                print(data['output'])
        else:
            pass
