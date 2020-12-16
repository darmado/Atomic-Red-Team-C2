import uuid
from blackbot.core.wss.crypto import gen_stager_psk
from blackbot.core.wss.stager import Stager
from blackbot.core.utils import get_path_in_package


class ARTIC2Stager(Stager):
    def __init__(self):
        self.name = 'dll'
        self.description = 'Generates a windows dll stager'
        self.suggestions = ''
        self.extension = 'dll'
        self.last_updated_by = '@byt3bl33d3r'
        self.options = {}

    def generate(self, listener):
        with open(get_path_in_package('core/wss/data/naga.dll'), 'rb') as dll:
            guid = uuid.uuid4()
            psk = gen_stager_psk()

            return guid, psk, dll.read().decode('latin-1')
