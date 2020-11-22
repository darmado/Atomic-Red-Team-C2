import os
import importlib
import logging
from blackbot.core.utils import get_path_in_package

class Loader:
    def __init__(self, type="atomic", paths=[]):
        self.type = type
        self.paths = paths
        self.loaded = []
        self.obfuscation_wrappers = []
        self.tunnels = []

        self.get_loadables()
        self.get_obfuscation_wrappers()
        self.get_tunnels()

    def is_sane(self, ttp):
        return True

    def get_obfuscation_wrappers(self):
        (root, _, wrappers) = next(os.walk(get_path_in_package('core/obfuscate')))

        for wrapper in wrappers:
            if wrapper[-3:] == '.py':
                w = self.load(os.path.join(root, wrapper))
                current_obf = w.ARTIC2Wrapper().name
                if any(self.obfuscation_wrappers):
                    for obf in self.obfuscation_wrappers:
                        if obf.name == current_obf:
                            continue
                        else:
                            self.obfuscation_wrappers.append(w.ARTIC2Wrapper())
                else:
                    self.obfuscation_wrappers.append(w.ARTIC2Wrapper())

        return self.obfuscation_wrappers

    def get_tunnels(self):
        (root, _, filenames) = next(os.walk(get_path_in_package('core/wss/tunnels')))

        for tunnel in filenames:
            if tunnel[-3:] == '.py':
                w = self.load(os.path.join(root, tunnel))
                current_tunnel = w.ARTIC2Tunnel().name
                if any(self.tunnels):
                    for tunnel in self.tunnels:
                        if tunnel.name == current_tunnel:
                            continue
                        else:
                            self.tunnels.append(w.ARTIC2Tunnel())
                else:
                    self.tunnels.append(w.ARTIC2Tunnel())

        return self.tunnels

    def load(self, path):
        ttp_spec = importlib.util.spec_from_file_location(self.type, path)
        ttp = importlib.util.module_from_spec(ttp_spec)
        ttp_spec.loader.exec_module(ttp)
        self.is_sane(ttp)
        
        return ttp
    
    def get_loadables(self):
        self.loaded = []
        for path in self.paths:
            for ttp in os.listdir(path):
                if ttp[-3:] == '.py' and not ttp.startswith("example") and ttp != '__init__.py':
                    try:
                        m = self.load(os.path.join(path, ttp))
                        if self.type == 'listener':
                            self.loaded.append(m.ARTIC2Listener())
                        elif self.type == 'stager':
                            self.loaded.append(m.ARTIC2Stager())
                        elif self.type == 'atomic':
                            self.loaded.append(m.Atomic())
                    except Exception as e:
                        logging.error(f'Failed loading {self.type} {os.path.join(path, ttp)}: {e}')

        logging.debug(f"Loaded {len(self.loaded)} {self.type}(s)")
        return self.loaded
