#! /usr/bin/env python3

"""
Usage: artic2.py [-h] [-v] (client|wss) [<args>...]

options:
    -h, --help                   Show this help message and exit
    -v, --version                Show version

...............+
SERVER OPTIONS |
...............+
By default, WSS binds to port 5000

[] Start WSS on the default port and prouce adhoc log
   - artic2.py wss 127.0.0.1 Art1.c25rvr >> /var/log/artic2.log &

[] Start WSS on the default port in foreground
    - artic2.py wss 127.0.0.1 Art1.c25rvr'

[] Start WSS on the default port in foreground and bind to port 5443
    - artic2.py wss 127.0.0.1 Art1.c25rvr --port 5443



...............+
CLIENT OPTIONS |
...............+

[] Connect to WSS server on default port 5000
    + artic2.py client wss://operator:BArt1.c25rvr@127.0.0.1:5000

[] Connect to WSS server on custom port 5443
    + artic2.py client wss://operator:BArt1.c25rvr@127.0.0.1:5443


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
