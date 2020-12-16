from blackbot.core.ipcclient import IPCClient

class Listener(IPCClient):

    def __init__(self):
        super().__init__()
        self.name = ''
        self.last_updated_by = ''
        self.description = ''
        self.options = {}

    def __getitem__(self, key):
        for k,_ in self.options.items():
            if k.lower() == key.lower():
                return self.options[k]['Value']

    def __setitem__(self, key, value):
        for k,_ in self.options.items():
            if k.lower() == key.lower():
                self.options[k]['Value'] = value

    def __iter__(self):
        yield ("name", self.name)
        yield ("last_updated_by", self.last_updated_by)
        yield ("description", self.description)
        yield ("running", self.running)
        yield ("options", self.options)
