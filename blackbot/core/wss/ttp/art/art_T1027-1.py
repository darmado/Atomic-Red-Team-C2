from blackbot.core.utils import get_path_in_package
from blackbot.core.wss.atomic import Atomic
from terminaltables import SingleTable
import os
import json

class Atomic(Atomic):
    def __init__(self):
        self.name = 'DefenseEvasion/T1027-1'
        self.controller_type = ''
        self.external_id = 'T1027'
        self.blackbot_id = 'T1027-1'
        self.version = ''
        self.language = 'boo'
        self.description = self.get_description()
        self.last_updated_by = 'Blackbot, Inc. All Rights reserved'
        self.references = ["System.Management.Automation"]
        self.options = {
                'OutString': {
                    'Description'   :   'Appends Out-String to the PowerShellCode',
                    'Required'      :   False,
                    'Value'         :   True,
                },
                'BypassLogging': {
                    'Description'   :   'Bypasses ScriptBlock and Techniques logging',
                    'Required'      :   False,
                    'Value'         :   True,
                },
                'BypassAmsi': {
                    'Description'   :   'Bypasses AMSI',
                    'Required'      :   False,
                    'Value'         :   True,
                }
            }

    def payload(self):
        with open(get_path_in_package('core/wss/ttp/art/src/powershell.boo'), 'r') as ttp_src:
            src = ttp_src.read()
            pwsh_script = get_path_in_package('core/wss/ttp/art/pwsh_ttp/defenseEvasion/T1027-1')

            with open(pwsh_script) as pwsh:
                src = src.replace("POWERSHELL_SCRIPT", pwsh.read())
                src = src.replace("OUT_STRING", str(self.options["OutString"]["Value"]).lower())
                src = src.replace("BYPASS_LOGGING", str(self.options["BypassLogging"]["Value"]).lower())
                src = src.replace("BYPASS_AMSI", str(self.options["BypassAmsi"]["Value"]).lower())

                return src

    def get_description(self):
        path = get_path_in_package('core/wss/ttp/art/pwsh_ttp/defenseEvasion/T1027-1')

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




