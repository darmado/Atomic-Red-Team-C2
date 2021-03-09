import logging
import functools
import shlex
import asyncio
import shutil
import importlib
from typing import List
from docopt import docopt, DocoptExit
from terminaltables import SingleTable
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.styles import Style
from prompt_toolkit.document import Document
from blackbot.core.client.contexts.wss import WSServer
from blackbot.core.client.utils import command, register_cli_commands
from blackbot.core.utils import print_bad, print_good, print_info, get_path_in_package
import sys
import os
from blackbot.core.client.event_handlers import witness
from blackbot.core.utils import gen_random_string_no_digits

from blackbot.core.wss.db import AsyncARTIC2db

example_style = Style.from_dict({
    'rprompt': 'bg:#ff0066 #ffffff',
})

def bottom_toolbar(ts):
    if ts.selected and ts.selected.stats.CONNECTED:
        ts = ts.selected
        terminal_width,_ = shutil.get_terminal_size()
        info_bar1 = f"{ts.alias} - {ts.url.scheme}://{ts.url.username}@{ts.url.hostname}:{ts.url.port}"
        info_bar2 = f"[Sessions: {len(ts.stats.SESSIONS)} Listeners: {len(ts.stats.LISTENERS)} Users: {len(ts.stats.USERS)}]"
        ljustify_amount = terminal_width - len(info_bar2)
        return HTML(f"{info_bar1:<{ljustify_amount}}{info_bar2}")
    else:
        return HTML('<b><style bg="ansired">Disconnected</style></b>')

def get_rprompt(error=False):
    return HTML('(<b><ansired>Error</ansired></b>)') if error else ''

class ARTIC2Completer(Completer):
    def __init__(self, cli_menu):
        self.path_completer = PathCompleter()
        self.cli_menu = cli_menu
        
        (_, _, attack_chain_files) = next(os.walk(get_path_in_package('core/automate/attack_chain')))
        (_, _, attack_profile_files) = next(os.walk(get_path_in_package('core/automate/attack_profile')))
        (_, _, attack_scenario_files) = next(os.walk(get_path_in_package('core/automate/attack_scenario')))

        self.attack_chain_files = attack_chain_files 
        self.attack_profile_files = attack_profile_files
        self.attack_scenario_files = attack_scenario_files

        self.stagers_path = '/var/www/html'


    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor()
        try:
            cmd_line = list(map(lambda s: s.lower(), shlex.split(document.current_line)))
        except ValueError:
            pass
        else:
            if len(cmd_line):
                if cmd_line[0] == 'attackchain' or cmd_line[0] == 'attackprofile' or cmd_line[0] == 'attackscenario':
                    if cmd_line[0] == 'attackchain':
                        filenames = self.attack_chain_files
                    elif cmd_line[0] == 'attackprofile':
                        filenames = self.attack_profile_files 
                    elif cmd_line[0] == 'attackscenario':
                        filenames = self.attack_scenario_files 
                   
                    try:
                        if cmd_line[1] in filenames:
                            for session in self.cli_menu.wsserver.selected.stats.SESSIONS.values():
                                if session['alias'].startswith(word_before_cursor):
                                    yield Completion(session['alias'], -len(word_before_cursor))
                            return
                    except:
                        pass

                    for f in filenames:
                        if word_before_cursor.lower() in f.lower():
                            try:
                                yield Completion(f, -len(cmd_line[1]))
                            except IndexError:
                                yield Completion(f, -len(word_before_cursor))
                    return

                if self.cli_menu.current_context.name == 'wsserver':
                    if cmd_line[0] in self.cli_menu.current_context._cmd_registry:
                        for conn in self.cli_menu.current_context.connections:
                            if conn.alias.startswith(word_before_cursor):
                                yield Completion(conn.alias, -len(word_before_cursor))

                if self.cli_menu.wsserver.selected:    
                    if cmd_line[0] == 'use':
                        if hasattr(self.cli_menu.current_context, 'available'):
                            ordered_list = sorted(self.cli_menu.current_context.available)
                            for loadable in ordered_list:
                                if word_before_cursor.upper() in loadable.upper():
                                    try:
                                        yield Completion(loadable, -len(cmd_line[1]))
                                    except IndexError:
                                        yield Completion(loadable, -len(word_before_cursor))
                            return

                    if cmd_line[0] == 'tunnel':
                        try:
                            if cmd_line[1] in [t.name for t in self.cli_menu.current_context.tunnels]:
                                (_, _, filenames) = next(os.walk(self.stagers_path))
                                for stager_file in filenames:
                                    if stager_file.startswith(word_before_cursor):
                                        yield Completion(stager_file, -len(word_before_cursor))
                                return
                        except:
                            pass
                        
                        for name in [t.name for t in self.cli_menu.current_context.tunnels]:
                            if name.startswith(word_before_cursor):
                                yield Completion(name, -len(word_before_cursor))
                        return
                    
                    if cmd_line[0] == 'obfuscate':
                        try:
                            if cmd_line[1] in [n.name for n in self.cli_menu.current_context.obfuscation_wrappers]:
                                (_, _, filenames) = next(os.walk(self.stagers_path))
                                for stager_file in [s for s in filenames if s.split('.')[1] == cmd_line[1]]:
                                    if stager_file.startswith(word_before_cursor):
                                        yield Completion(stager_file, -len(word_before_cursor))
                                return
                        except:
                            pass

                        for name in [w.name for w in self.cli_menu.current_context.obfuscation_wrappers]:
                            if name.startswith(word_before_cursor):
                                yield Completion(name, -len(word_before_cursor))
                        return
                    
                    if hasattr(self.cli_menu.current_context, 'selected') and self.cli_menu.current_context.selected:
                        if cmd_line[0] == 'set':
                            if len(cmd_line) >= 2 and cmd_line[1] == 'bindip':
                                for ip in self.cli_menu.wsserver.selected.stats.IPS:
                                    if ip.startswith(word_before_cursor):
                                        yield Completion(ip, -len(word_before_cursor))

                                return

                            try:
                                if cmd_line[1] == 'atomic':
                                    for ttp in self.cli_menu.current_context.selected['ttp_list']:
                                        if ttp.lower().startswith(word_before_cursor.lower()):
                                            yield Completion(ttp, -len(word_before_cursor))
                                    return

                            except:
                                pass

                            for option in self.cli_menu.current_context.selected['options'].keys():
                                if option.lower().startswith(word_before_cursor.lower()):
                                    yield Completion(option, -len(word_before_cursor))
                            return

                        elif cmd_line[0] == 'generate':
                            for listener in self.cli_menu.wsserver.selected.stats.LISTENERS.keys():
                                if listener.startswith(word_before_cursor):
                                    yield Completion(listener, -len(word_before_cursor))

                            return
                       
                        elif cmd_line[0] in ['run', 'info', 'sleep', 'kill', 'jitter', 'checkin', 'rename']:
                            for session in self.cli_menu.wsserver.selected.stats.SESSIONS.values():
                                if session['alias'].startswith(word_before_cursor):
                                    yield Completion(session['alias'], -len(word_before_cursor))

                            return

            if hasattr(self.cli_menu.current_context, "_cmd_registry"):
                for cmd in self.cli_menu.current_context._cmd_registry:
                    if cmd.startswith(word_before_cursor):
                        yield Completion(cmd, -len(word_before_cursor))

            for ctx in self.cli_menu.get_context():
                if ctx.name.startswith(word_before_cursor) and ctx.name is not self.cli_menu.current_context.name:
                    yield Completion(ctx.name, -len(word_before_cursor))

            if self.cli_menu.current_context.name != 'main':
                for cmd in self.cli_menu._cmd_registry:
                    if cmd.startswith(word_before_cursor):
                        yield Completion(cmd, -len(word_before_cursor))
            
@register_cli_commands
class ARTIC2Shell:
    name = 'main'
    description = 'Command'

    _remote = False

    def __init__(self, args):
        self.args = args
        self.current_context = self
        self.attack_is_ready = False
        self.prompt = None

        self.wsserver = WSServer(args['<URL>'])

        self.completer = ARTIC2Completer(self)
        self.prompt_session = PromptSession(
            HTML(
                "<ansiwhite>"
                 f"T{len(self.wsserver.connections)}"
                 "</ansiwhite>"

                "<ansired> ARTi-c2/main :≫ "
                 f"</ansired>"
            ),
            bottom_toolbar=functools.partial(bottom_toolbar, ts=self.wsserver),
            completer=self.completer,
            complete_in_thread=True,
            complete_while_typing=True,
            auto_suggest=AutoSuggestFromHistory(),
            search_ignore_case=True
        )

    def get_context(self, ctx_name=None):
        try:
            cli_menus = [*self.wsserver.selected.contexts, self.wsserver]
        except AttributeError:
            cli_menus = [self.wsserver]

        if ctx_name:
            return list(filter(lambda c: c.name == ctx_name, cli_menus))[0]

        return cli_menus

    def patch_badchar(self, args, patch=False):
        if patch:
            for key, value in args.items():
                if key == '<value>':
                    args[key] = "-" + value
                    return args
        else:
            try:
                if (args[2][0] == '-'):
                    args[2] = args[2][1:]
                    return True, args
                return False, args
            except IndexError:
                return False, args

    async def update_prompt(self, ctx):
        self.prompt_session.message = HTML(
            ("<ansired>"
             f"T{len(self.wsserver.connections)}"
             f"</ansired> ARTi-c2/{ctx.name} :≫<ansired></ansired> {' ' if not ctx.prompt else ctx.prompt + ' ' }")
        )

    async def switched_context(self, text):
        for ctx in self.get_context():
            if text.lower() == ctx.name:
                if ctx._remote is True:
                    try:
                        response = await self.wsserver.send(
                                ctx=ctx.name,
                                cmd="get_selected"
                            )
                        if response.result:
                            ctx.selected = response.result
                    except AttributeError:
                        break

                await self.update_prompt(ctx)
                self.current_context = ctx
                return True
        return False

    async def parse_command_line(self, text):
        if not await self.switched_context(text):
            try:
                command = shlex.split(text)
                needs_patch, command = self.patch_badchar(command)

                args = docopt(
                    getattr(self.current_context if hasattr(self.current_context, command[0]) else self, command[0]).__doc__,
                    argv=command[1:]
                )

                if needs_patch:
                    args = self.patch_badchar(args, patch=True)
            except ValueError as e:
                print_bad(f"Error parsing command: {e}")
            except AttributeError as e:
                print_bad(f"Unknown command '{command[0]}'")
            except (DocoptExit, SystemExit):
                pass
            else:
                if command[0] in self._cmd_registry or self.current_context._remote is False:
                    run_in_terminal(
                        functools.partial(
                            getattr(self if command[0] in self._cmd_registry else self.current_context, command[0]),
                            args=args
                        )
                    )

                elif self.current_context._remote is True:
                    response = await self.wsserver.send(
                            ctx=self.current_context.name,
                            cmd=command[0],
                            args=args
                        )

                    if response.status == 'success' and response.result:
                        if hasattr(self.current_context, command[0]):
                            run_in_terminal(
                                functools.partial(
                                    getattr(self.current_context, command[0]),
                                    args=args,
                                    response=response
                                )
                            )

                    elif response.status == 'error':
                        print_bad(response.result)

                if self.current_context.name != 'main':
                    await self.update_prompt(self.current_context)

    async def run_automate_file(self, automated_attack_file, session=None):
        with open(automated_attack_file) as automate_file:
            for cmd in automate_file:
                if session != None:
                    if cmd[0:3] == 'run':
                        session_target = ' '.join(session)
                        cmd = cmd.replace(cmd.split(' ')[1], session_target)

                    elif cmd[0:13] == 'attackprofile':
                        path = get_path_in_package('core/automate/attack_profile/verified')
                       
                        INSTRUCTIONS = '{}/{}'.format(path, cmd.split(' ')[1].strip('\n'))
                        SESSION = session
                        
                        await asyncio.sleep(1)
                        await self.ExecuteAttack(INSTRUCTIONS, SESSION) 
                        continue

                    elif cmd[0:11] == 'attackchain':
                        path = get_path_in_package('core/automate/attack_chain/verified')
                       
                        INSTRUCTIONS = '{}/{}'.format(path, cmd.split(' ')[1].strip('\n'))
                        SESSION = session
                        
                        await asyncio.sleep(1)
                        await self.ExecuteAttack(INSTRUCTIONS, SESSION) 
                        continue
                    
                with patch_stdout():
                    try:
                        text = await self.prompt_session.prompt_async(accept_default=True, default=cmd.strip())
                    
                    except AssertionError:
                        text = cmd.strip()
                    
                    if text.lower() == 'exit':
                        loop = asyncio.get_event_loop()
                        loop.create_task(self.wsserver.selected.ws.close())
                        sys.exit()
                    
                    await asyncio.sleep(1)
                    await self.parse_command_line(text)

    async def cmdloop(self):
        if self.args['--automate']:
            if self.wsserver.selected:
                await asyncio.sleep(1)
                await self.run_automate_file(self.args['--automate'])

        while True:
            with patch_stdout():
                text = await self.prompt_session.prompt_async()
                if len(text):
                    if text.lower() == 'exit':
                        loop = asyncio.get_event_loop()
                        loop.create_task(self.wsserver.selected.ws.close())
                        break

                    await self.parse_command_line(text)
                    
                    await asyncio.sleep(0.02)
                    if self.attack_is_ready:
                        await self.ExecuteAttack(INSTRUCTIONS, SESSION) 

    @command
    def help(self):
        """
        Shows available commands

        Usage: help

        """
        table_data = [
            ["Command", "Description"]
        ]

        try:
            for cmd in self.current_context._cmd_registry:
                table_data.append([cmd, getattr(self.current_context, cmd).__doc__.split('\n', 2)[1].strip()])

            for menu in self.get_context():
                if menu.name != self.current_context.name:
                    table_data.append([menu.name, menu.description])

        except AttributeError:
            for menu in self.get_context():
                table_data.append([menu.name, menu.description])

        table = SingleTable(table_data)
        print(table.table)

    async def ExecuteAttack(self, automated_attack_file, session):
        await self.run_automate_file(automated_attack_file, session=session)
        self.attack_is_ready = False
        SESSION = None
        INSTRUCTIONS = ''

    @command
    def attackscenario(self, automated_attack_file: str, sessions: List[str]):
        """
        Runs an attackscenario file

        Usage: attackscenario [-h] <automated_attack_file> <sessions>...
        """
        global INSTRUCTIONS
        global SESSION

        path = 'core/automate/attack_scenario'
        automated_attack_file = get_path_in_package('{}/{}'.format(path, automated_attack_file))
        
        if os.path.exists(automated_attack_file):
            self.attack_is_ready = True
            INSTRUCTIONS = automated_attack_file
            SESSION = sessions

        else:
            print(' * [!] No such attack scenario.')

    @command
    def attackprofile(self, automated_attack_file: str, sessions: List[str]):
        """
        Runs an attackprofile file

        Usage: attackprofile [-h] <automated_attack_file> <sessions>...
        """
        global INSTRUCTIONS
        global SESSION

        path = 'core/automate/attack_profile/'
        automated_attack_file = get_path_in_package('{}/{}'.format(path, automated_attack_file))
        
        if os.path.exists(automated_attack_file):
            self.attack_is_ready = True
            INSTRUCTIONS = automated_attack_file
            SESSION = sessions

        else:
            print(' * [!] No such attack profile.')

    @command
    def attackchain(self, automated_attack_file: str, sessions: List[str]):
        """
        Runs an attackchain file

        Usage: attackchain [-h] <automated_attack_file> <sessions>...
        """
        global INSTRUCTIONS
        global SESSION

        path = 'core/automate/attack_chain/'
        automated_attack_file = get_path_in_package('{}/{}'.format(path, automated_attack_file))
        
        if os.path.exists(automated_attack_file):
            self.attack_is_ready = True
            INSTRUCTIONS = automated_attack_file
            SESSION = sessions

        else:
            print(' * [!] No such attack chain.')

    @command
    def decodeevidence(self, option: str):
        """
        Display the evidence decoded in the screen
        
        Option: 'on' / 'off'
        
        Usage: decodeevidence [-h] <option>
        """
        witness.setStatus(option)

    @command
    def back(self):
        """
        Go back to the main menu.

        Usage: back [-h]
        """
        self.current_context = self
        asyncio.create_task(self.update_prompt(self.current_context))

