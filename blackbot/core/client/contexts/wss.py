import asyncio
import logging
from typing import List
from blackbot.core.client.connection import ClientConnection
from blackbot.core.utils import gen_random_string, print_info, print_bad
from blackbot.core.client.utils import command, register_cli_commands
from terminaltables import SingleTable


@register_cli_commands
class WSServer:
    name  = 'wss'
    description = 'WEB SOCKET MENU'

    _remote = False

    def __init__(self, urls=[]):
        self.prompt = None

        self.connections = [ClientConnection(url) for url in urls]
        self.selected = self.connections[0] if len(self.connections) else None

        for wss in self.connections:
            wss.start()

    async def send(self, ctx, cmd, args={}, data={}):
        if self.selected and self.selected.stats.CONNECTED:
            normalized_args = {}
            for k,v in args.items():
                if k in ['-h', '--help']:
                    continue
                elif k.startswith("<"):
                    normalized_args[k[1:-1]] = v
                elif k.startswith("--"):
                    normalized_args[k[2:]] = v

            message = {
                "id" : gen_random_string(),
                "ctx": ctx,
                "cmd": cmd,
                "args": normalized_args,
                "data": data
            }

            return await self.selected.send(message)

        print_bad("Not connected to a Web Socket URL")

    @command
    def connect(self, URL: List[str]):
        """
        Connect to the specified Web Socket URL(s)

        Usage: connect [-h] <URL>...

        Arguments:
            URL   Web Socket URL url(s)
        """

        for url in URL:
            conn = ClientConnection(url)
            conn.start()
            self.connections.append(conn)
            if not self.selected: self.selected = conn

    @command
#    def disconnect(self, TS: List[str]):
#        """
#        Disconnect from the specified Web Socket URL(s)
#
#        Usage: disconnect [-h] <TS>...
#
#        Arguments:
#            TS  Web Socket URL(s) to disconnect from
#        """
#
#        for wss in self.connections:
#            for to_disconnect in TS:
#                if wss.alias == to_disconnect:
#                    wss.stop()
#                    self.selected = None
#                    del self.connections[self.connections.index(wss)]

#    @command
    def use(self, TS: str):
        """
        Select a specified Web Socket URL for all communication

        Usage: use [-h] <TS>

        Arguments:
            WSS   Web Socket URL to use
        """

        for wss in self.connections:
            if wss.alias == WSS:
                self.selected = wss
                print_info(f"Now using {ts.alias} for all comms")
                return

        print_bad(f"Not currently connected to WSS Server '{WSS}'")

    @command
    def rename(self, old_name: str, new_name: str):
        """
        Rename a specified Web Socket URL

        Usage: use [-h] <old_name> <new_name>

        Arguments:
            old_name   old WSS URL name
            new_name   new WSS URL name
        """
        for wss in self.connections:
            if wss.alias == old_name:
                wss.alias = new_name
                print_info(f"Renamed Web Socket URL {old_name} to {new_name}")
                break

    @command
    def list(self):
        """
        Show available Web Socket URL

        Usage: list [-h]

        """
        if self.connections:
            table_data = [["Alias", "WEB SOCKET URL"]]
            for conn in self.connections:
                table_data.append([f"*{conn.alias}" if self.selected == conn else conn.alias, str(conn)])

            table = SingleTable(table_data, title='WSS SERVERS')
            table.inner_row_border = True
            print(table.table)
