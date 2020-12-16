import asyncio
import logging
from typing import List
from blackbot.core.client.utils import command, register_cli_commands
from terminaltables import SingleTable
from time import gmtime, strftime
from blackbot.core.utils import get_path_in_package

@register_cli_commands
class Atomic:
    name = 'atomic'
    description = '≫ ATOMIC RED TEAM TECHNIQUES'
    
    _remote = True

    def __init__(self):
        self.prompt = None
        self.available = []
        self._selected = None
    
    
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
        Use specific ART Tactic

        Usage: use <name> [-h]

        Arguments:
            name  ttp to select
        """

        self.selected = response.result

    @command
    def list(self, name: str, response):
        """
        List loaded ART Tactics & Techniques

        Usage: list [-h] [<name>]

        Arguments:
            name   filter by ttp name
        """
      
        table_data = [['Name', 'Description']]
        for m_name, m_description in response.result.items():
            table_data.append([m_name, m_description])

        table = SingleTable(table_data, title="Techniques")
        table.inner_row_border = False
        
        print(table.table)

    @command
    def options(self, response):
        """
        Describe options for loaded ART Tactic

        Usage: options [-h]
        """

        table_data = [["Option Name", "Required", "Value", "Description"]]
        for k, v in response.result.items():
            table_data.append([k, v["Required"], v["Value"], v["Description"]])

        table = SingleTable(table_data, title=self.selected['name'])
        table.inner_row_border = True
        print(table.table)

    @command
    def info(self, response):
        """
        Print ART Technique IDs for loaded Tactic 

        Usage: options [-h]
        """
        print("")
        
        print(f"Description: {response.result['description']}\n")

        table_data = [["Option Name", "Required", "Value", "Description"]]
        for k, v in response.result['options'].items():
            table_data.append([k, v["Required"], v["Value"], v["Description"]])

        table = SingleTable(table_data, title=self.selected['name'])
        table.inner_row_border = False
        
        print(table.table)

    @command
    def run(self, guids: List[str], response):
        """
        Execute loaded technique on specific target ssession ID

        Usage:
            run <guids>...
            run -h | --help

        Arguments:
            guids    session guids to run ttp on 
                     (specifying 'all' will run ttp on all sessions)

        Options:
            -h, --help   Show dis
        """
        pass

    @command
    def reload(self, response):
        """
        Reload All ART Tactics

        Usage: reload [-h]
        """
        pass

    @command
    def set(self, name: str, value: str, response):
        """
        Set ART technique ID from info option

        Usage: set <name> <value> [-h]

        Arguments:
            name   option name
            value  option value
        """
        pass
    
