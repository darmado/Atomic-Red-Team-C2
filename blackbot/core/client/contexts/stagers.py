import asyncio
import logging
from terminaltables import SingleTable
from blackbot.core.utils import print_good, gen_random_string
from blackbot.core.client.utils import command, register_cli_commands
from blackbot.core.wss.loader import Loader

@register_cli_commands
class Stagers:
    name = 'stagers'
    description = 'Stagers menu'

    _remote = True

    def __init__(self):
        self.prompt = None
        self.available = []
        self._selected = None

        self.obfuscation_wrappers = Loader().get_obfuscation_wrappers()
        self.tunnels = Loader().get_tunnels()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, data):
        self.prompt = f"(<ansired>{data['name']}</ansired>)"
        self._selected = data

    @command
    def use(self, name: str, response):
        """
        Select the specified stager

        Usage: use <name> [-h]

        Arguments:
            name  filter by stager name
        """

        self.selected = response.result

    @command
    def list(self, response):
        """
        List available stagers

        Usage: list [-h]
        """
        table_data = [["Name", "Description"]]
        ordered_list = sorted(response.result.items(), key = lambda x: x[0])
        for name,fields in ordered_list:
            table_data.append([name, fields["description"]])

        table = SingleTable(table_data, title="Available")
        table.inner_row_border = True
        print(table.table)

    @command
    def options(self, response):
        """
        Show selected stager options

        Usage: options [-h]
        """

        table_data = [
            ["Option Name", "Required", "Value", "Description"]
        ]
        for k, v in response.result.items():
            table_data.append([k, v["Required"], v["Value"], v["Description"]])

        table = SingleTable(table_data, title="Stager Options")
        table.inner_row_border = True
        print(table.table)

    @command
    def obfuscate(self, target_type: str, stager_name: str, response):
        """
        Obfuscate the stager code based on its type, using a third part tool

        Usage: obfuscate [-h] <target_type> <stager_name>
        """
        pass

    @command
    def generate(self, listener_name: str, location: str, response):
        """
        Generate the selected stager

        Usage: generate [-h] <listener_name> <location>
        
        Arguments:
            listener_name   listener name
            location        physical location
        """
        stager_name = gen_random_string()

        generated_stager = response.result
        
        stager_filename = f"/var/www/html/{stager_name}.{generated_stager['extension']}"
        with open(stager_filename, 'wb') as stager:
            stager.write(generated_stager['output'].encode('latin-1'))

        print_good(f"Generated stager to {stager_filename}")

    @command
    def set(self, name: str, value: str, response):
        """
        Set options on the selected listener

        Usage: set <name> <value> [-h]

        Arguments:
            name   option name
            value  option value
        """

    @command
    def reload(self, response):
        """
        Reload all ttp

        Usage: reload [-h]
        """
    
    @command
    def tunnel(self, tunnel_name: str, target: str, response):
        """
        Open tunnels to stager deployment

        Usage: tunnel [-h] <tunnel_name> <target>
        """
        urls = response.result
        print(urls)
