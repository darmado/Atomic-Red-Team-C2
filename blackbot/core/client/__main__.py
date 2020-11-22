#!/usr/bin/env python3

"""
Usage: client [-h] [-d] [--automate <FILE>] [<URL>...]

arguments:
    URL   wss url(s)

options:
    -h, --help                   Show this help message and exit
    -r, --automate <FILE>        Read automate profile
    -d, --debug                  Enable debug output
"""

import logging
import asyncio
from blackbot import VERSION, CODENAME
from blackbot.core.utils import print_banner
from blackbot.core.client.cmdloop import ARTIC2Shell

async def main(args):
    s = ARTIC2Shell(args)
    print_banner(CODENAME, VERSION)
    await s.cmdloop()

def start(args):
    log_level = logging.DEBUG if args['--debug'] else logging.INFO
    logging.basicConfig(format="%(asctime)s [%(levelname)s] - %(filename)s: %(funcName)s - %(message)s", level=log_level)
    logging.getLogger('websockets').setLevel(log_level)
    asyncio.run(main(args))
