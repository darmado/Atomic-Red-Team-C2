#!/usr/bin/env python3

"""
Usage: wss [-h] [--port <PORT>] [--insecure] <host> <password>

optional arguments:
    -h, --help          Show this help message and exit
    -p, --port <PORT>   Port to bind to [default: 5000]
    --insecure          Start server without TLS
"""

import asyncio
import json
import logging
import os
import os.path
import ssl
import websockets
import signal
import http
import functools
import hmac
import traceback
from termcolor import colored
from base64 import b64decode
from websockets import WebSocketServerProtocol
from hashlib import sha512
from typing import Dict, List, Any
from blackbot.core.events import Events
from blackbot.core.wss.db import AsyncARTIC2db
from blackbot.core.wss.users import Users, UsernameAlreadyPresentError
from blackbot.core.wss.contexts import Listeners, Sessions, Stagers, Atomic
from blackbot.core.utils import create_self_signed_cert, get_cert_fingerprint, decode_auth_header, \
    CmdError, get_ips, get_data_folder, get_path_in_data_folder, get_path_in_artic2

class WSS:
    def __init__(self):
        self.users = Users()
        self.loop = asyncio.get_running_loop()
        self.contexts = {
            'listeners': Listeners(self),
            'sessions': Sessions(self),
            'stagers': Stagers(self),
            'atomic': Atomic(self),
            'users': self.users
        }

    async def process_client_message(self, user, path, data):
        message = json.loads(data)
        logging.debug(f"Received message from {user.name}@{user.ip} path:{path} msg: {message}")
        status = 'error'

        try:
            ctx = self.contexts[message['ctx'].lower()]
        except KeyError:
            traceback.print_exc()
            result = f"Context '{message['ctx'].lower()}' does not exist"
            logging.error(result)
        else:
            try:
                cmd_handler = getattr(ctx, message['cmd'])
                result = cmd_handler(**message['args'])
                status = 'success'
            except AttributeError:
                traceback.print_exc()
                result = f"Command '{message['cmd']}' does not exist in context '{message['ctx'].lower()}'"
            except CmdError as e:
                result = str(e)
            except Exception as e:
                traceback.print_exc()
                result = f"Exception when executing command '{message['cmd']}': {e}"
                logging.error(result)

        await user.send({
                'type': 'message',
                'id': message['id'],
                'ctx': message['ctx'],
                'name': message['cmd'],
                'status': status,
                'result': result
        })

    async def update_server_stats(self):
        stats = {**{str(ctx): dict(ctx) for ctx in self.contexts.values()}, 'ips': get_ips()} 
        await self.users.broadcast_event(Events.STATS_UPDATE, stats)

    async def update_available_loadables(self):
        loadables = {str(ctx): [loadable.name for loadable in ctx.loaded] for ctx in self.contexts.values() if hasattr(ctx, 'loaded')}
        await self.users.broadcast_event(Events.LOADABLES_UPDATE, loadables)

    async def connection_handler(self, websocket, path):
        try:
            user = await self.users.register(websocket)
            await self.update_server_stats()
            await self.update_available_loadables()
            logging.info(f"New client connected {user.name}@{user.ip}")
        except UsernameAlreadyPresentError as e:
            logging.error(f"{websocket.remote_address[0]}: {e}")
            return

        while True:
            try:
                data = await asyncio.wait_for(websocket.recv(), timeout=20)
            except asyncio.TimeoutError:
                logging.debug(f"No data from {user.name}@{user.ip} after 20 seconds, sending ping")
                try:
                    pong_waiter = await websocket.ping()
                    await asyncio.wait_for(pong_waiter, timeout=10)
                except asyncio.TimeoutError:
                    logging.debug(f"No pong from {user.name}@{user.ip} after 10 seconds, closing connection")
                    self.users.unregister(user.name)
                    await self.update_server_stats()
                    return

            except websockets.exceptions.ConnectionClosed:
                logging.debug(f"Connection closed by client")
                self.users.unregister(user.name)
                await self.update_server_stats()
                return
            else:
                await self.process_client_message(user, path, data)


class ARTIC2WebSocketServerProtocol(WebSocketServerProtocol):
    wss_digest = None

    async def process_request(self, path, request_headers):
        try:
            username, password_digest = decode_auth_header(request_headers)
            if not hmac.compare_digest(password_digest,ARTIC2WebSocketServerProtocol.wss_digest):
                logging.error(f"User {username} failed authentication")
                return http.HTTPStatus.UNAUTHORIZED, [], b'UNAUTHORIZED\n'
        except KeyError:
            logging.error('Received handshake with no last_updated_byization header')
            return http.HTTPStatus.FORBIDDEN, [], b'FORBIDDEN\n'

        logging.info(f"User {username} authenticated successfully")


async def server(stop, args, wss_digest):
    if not os.path.exists(get_path_in_artic2("artic2.db")):
        logging.info('Creating database')
        await AsyncARTIC2db.create_db_and_schema()

    ts = WSS()

    ssl_context = None
    if not args['--insecure']:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        try:
            ssl_context.load_cert_chain(
                get_path_in_data_folder("artic2_chain.pem")
            )
        except FileNotFoundError:
            create_self_signed_cert()
            ssl_context.load_cert_chain(
                get_path_in_data_folder("artic2_chain.pem")
            )

        server_cert_fingerprint = get_cert_fingerprint(get_path_in_data_folder("artic2_cert.pem"))
        logging.warning(
            (f"{colored('WSS certificate fingerprint:', 'yellow')} "
             f"{colored(server_cert_fingerprint.hex(), 'red')}")
        )

    ARTIC2WebSocketServerProtocol.wss_digest = wss_digest
    async with websockets.serve(
        ts.connection_handler,
        host=args['<host>'],
        port=int(args['--port']),
        create_protocol=ARTIC2WebSocketServerProtocol,
        ssl=ssl_context,
        ping_interval=None,
        ping_timeout=None
    ):

        logging.info(colored(f"WSS started on {args['<host>']}:{args['--port']}", "yellow"))

        await stop

def start(args):
    if not os.path.exists(get_path_in_artic2('logs')):
        logging.info("First time use detected, creating data folder")
        os.mkdir(get_path_in_artic2('logs'))

    loop = asyncio.get_event_loop()
    #wss_digest = hmac.new(args['<password>'].encode(), msg=b'at0m1cR3dT3amInt3ll1g3nc3C2', digestmod=sha512).hexdigest()
    wss_digest = hmac.new(args['<password>'].encode(), msg=b'blackbot', digestmod=sha512).hexdigest()

    stop = asyncio.Future()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set_result, None)

    if args['--insecure']:
        logging.warning('SECURITY WARNING: --insecure flag passed, communication between client and server will be in cleartext!')

    loop.run_until_complete(server(stop, args, wss_digest))
