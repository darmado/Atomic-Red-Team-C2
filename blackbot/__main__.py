#! /usr/bin/env python3

"""
Usage: st [-h] [-v] (client|wss) [<args>...]

options:
    -h, --help                   Show this help message and exit
    -v, --version                Show version
"""

from docopt import docopt
from blackbot import VERSION

def run():
    args = docopt(__doc__, version=VERSION, options_first=True)
    if args['client']:
        import blackbot.core.client.__main__ as client
        client.start(docopt(client.__doc__, argv=args["<args>"]))
    elif args['wss']:
        import blackbot.core.wss.__main__ as wss
        wss.start(docopt(wss.__doc__, argv=args["<args>"]))
