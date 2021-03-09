from blackbot.core.utils import get_path_in_package
from blackbot.core.wss.atomic import Atomic
from terminaltables import SingleTable

import os
import json

class Atomic(Atomic):
    def __init__(self):
        self.name = 'CredentialAccess/T1003.003-6'
        self.controller_type = ''
        self.external_id = 'T1003.003'
        self.blackbot_id = 'T1003.003-6'
        self.version = ''
        self.language = 'boo'
        self.description = self.get_description()
        self.last_updated_by = 'Blackbot, Inc. All Rights reserved'
        self.references = ["System.Management.Automation"]
        self.options = {}

    def payload(self):
        with open(get_path_in_package('core/wss/ttp/art/src/cmd_prompt.boo'), 'r') as ttp_src:
            src = ttp_src.read()
            cmd_script = get_path_in_package('core/wss/ttp/art/cmd_ttp/credentialAccess/T1003.003-6')

            with open(cmd_script) as cmd:
                src = src.replace("CMD_SCRIPT", cmd.read())
                
                return src

    def get_description(self):
        path = get_path_in_package('core/wss/ttp/art/cmd_ttp/credentialAccess/T1003.003-6')

        with open(path) as text:
            head = [next(text) for l in range(4)]
            technique_name = head[0].replace('#TechniqueName: ', '').strip('\n')
            atomic_name = head[1].replace('#AtomicTestName: ', '').strip('\n')
            description = head[2].replace('#Description: ', '').strip('\n')
            language = head[3].replace('#Language: ', '').strip('\n')

            aux = ''
            count = 1
            for char in description:
                if char == '&':
                    continue

                aux += char
                if count % 126 == 0:
                    aux += '\n'
                count += 1

            out = '{}: {}\n{}\n\n{}\n'.format(technique_name, language, atomic_name, aux)

        return out




