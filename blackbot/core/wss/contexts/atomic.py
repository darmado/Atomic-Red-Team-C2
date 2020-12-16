import types
import asyncio
from blackbot.core.events import Events
from blackbot.core.wss import ipc_server
from blackbot.core.wss.loader import Loader
from blackbot.core.utils import CmdError, get_path_in_package
from blackbot.core.wss.job import Job

class Atomic(Loader):
    name = 'atomic'
    description = """ARTIC2 Atomic Test Cases are a collection of adversary tactics and techniques based on real-world observations. The ATT&CK knowledge base is used as a foundation for the development of specific threat models and methodologies in the private sector, in government."""

    def __init__(self, wss):
        self.wss = wss
        self.ttp = []
        self.selected = None

        super().__init__(type="atomic", paths=[get_path_in_package("core/wss/ttp/art/")])

    def files_handlers(self):
        return {c.name: c.description for c in self.loaded}

    def list(self, name: str = None):
        return {c.name: c.description for c in self.loaded}

    def get_sessions(self):
        return c2.sessions()

    def use(self, name: str):
        for c in self.loaded:
            if c.name.lower() == name.lower():
                self.selected = c
                return dict(self.selected)

        raise CmdError(f"OPERATOR ERROR Message: use technique; status: TTP,  '{name.lower()}' is uknown")

    def options(self):
        if not self.selected:
            raise CmdError("OPERATOR ERROR Message: No module selected")
        return self.selected.options

    def info(self):
        if not self.selected:
            raise CmdError("OPERATOR ERROR Message: No module selected")
        return dict(self.selected)

    def set(self, name: str, value: str):
        if not self.selected:
            raise CmdError("OPERATOR ERROR Message: No module selected")

        try:
            self.selected[name] = value
        except KeyError:
            raise CmdError(f"OPERATOR ERROR Message:  Unknown Command '{name}'")

    def run(self, guids):
        for guid in guids:
            ipc_server.publish_event(Events.NEW_JOB, (guid, Job(module=self.selected)))
    
    def reload(self):
        self.get_loadables()
        if self.selected:
            self.use(self.selected.name)

        asyncio.create_task(
            self.wss.update_available_loadables()
        )

    def get_selected(self):
        if self.selected:
            return dict(self.selected)

    def __iter__(self):
        yield ('loaded', len(self.loaded))

    def __str__(self):
        return self.__class__.__name__.lower()
