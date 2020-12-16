import asyncio
import websockets
import hmac
import ssl
import logging
import pathlib
import json
import functools
from urllib.parse import urlparse
from base64 import b64encode
from websockets.http import Headers
from hashlib import sha512
from blackbot.core.utils import get_remote_cert_fingerprint, gen_random_string
from blackbot.core.client.stats import ClientConnectionStats
from blackbot.core.client.event_handlers import ClientEventHandlers
from blackbot.core.client.server_response import ServerResponse
from blackbot.core.client.contexts.listeners import Listeners
from blackbot.core.client.contexts.sessions import Sessions
from blackbot.core.client.contexts.atomic import Atomic
from blackbot.core.client.contexts.stagers import Stagers
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.application import run_in_terminal


class ClientConnection:
    def __init__(self, url: str):
        self.alias = f"TS-{gen_random_string(5)}"
        self.url = urlparse(url)
        self.stats = ClientConnectionStats()
        self.event_handlers = ClientEventHandlers(self)
        self.msg_queue =  asyncio.Queue(maxsize=1)
        self.contexts = [
            Listeners(),
            Sessions(),
            Stagers(),
            Atomic()
        ]
        self.task = None
        self.ws = None
        self.ssl_context = None
        

        if self.url.scheme == 'wss':
            self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.ssl_context.check_hostname = False
            self.ssl_context.verify_mode = ssl.CERT_NONE
        else:
            logging.warning('SECURITY WARNING: comms between client and server will be in cleartext!')

    def generate_auth_header(self, username, password):
        client_digest = hmac.new(password.encode(), msg=b'blackbot', digestmod=sha512).hexdigest()
        header_value = b64encode(f"{username}:{client_digest}".encode()).decode()
        return Headers({'Authorization': header_value})

    def start(self):
        def connect_callback(task):
            try:
                task.result()
            except asyncio.CancelledError:
                self.stats.CONNECTED = False
                logging.debug("ARTIC2 Connection task cancelled; status: not connected")
            except websockets.exceptions.InvalidStatusCode as e:
                logging.error(e)
                logging.error('ARTIC2 Authentication attempt failed; status: not authenticated; web socket: artic2')
            except ConnectionRefusedError as e:
                logging.error(e)
                logging.error('ARTIC2 Error  with artic2; status: not connected {self.url.scheme}://{self.url.hostname}:{self.url.port}"')

        self.task = asyncio.create_task(self.connect())
        self.task.add_done_callback(connect_callback)

    def stop(self):
        logging.warning(f"ARTIC2 Cancelling Connection Task; socket:{self.url.hostname}:{self.url.port}")
        self.task.cancel()

    async def connect(self):
        url = f"{self.url.scheme}://{self.url.hostname}:{self.url.port}"
        logging.debug(f'ARTIC2 status: connecting')
        while True:
            try:
                if self.url.scheme == 'wss':
                    server_cert_fingerprint = get_remote_cert_fingerprint(self.url.hostname, self.url.port)
                    logging.debug(
                            (f"ARTIC2 socket: {self.url.scheme}://{self.url.hostname}:{self.url.port}, ",f"cert_fingerprint: {server_cert_fingerprint.hex()} ")
                    )

                async with websockets.connect(
                    url, 
                    extra_headers=self.generate_auth_header(
                        self.url.username,
                        self.url.password
                    ), 
                    ssl=self.ssl_context, 
                    ping_interval=None,
                    ping_timeout=None
                ) as ws:
                    logging.info(f'status: connected')
                    self.stats.CONNECTED = True
                    self.ws = ws

                    await asyncio.wait([
                        self.data_handler(),
                        self.heartbeat()
                    ])
            except ConnectionRefusedError as e:
                logging.error(e)
                logging.error('ARTIC2 Error connecting to aft1: status: server not available')
                self.stats.CONNECTED = False

            await asyncio.sleep(5)

    async def data_handler(self):
        
        async for data in self.ws:
            data = json.loads(data)
            
            if data['type'] == "message":
                
                await self.msg_queue.put(data)

            elif data['type'] == 'event':
                
                try:
                    event_handler = functools.partial(
                        getattr(self.event_handlers, data['name'].lower()),
                        data=data['data']
                    )
                    with patch_stdout():
                        run_in_terminal(event_handler) 
                except AttributeError:
                    logging.error(f"status: Got event of unknown type '{data['name']}'")

        self.stats.CONNECTED = False
        logging.debug("data_handler has stopped")

    async def heartbeat(self):
        while self.ws.open: 
            try:
                pong_waiter = await self.ws.ping()
                await asyncio.wait_for(pong_waiter, timeout=20)
            except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                logging.error(e)
                logging.error("status: Disconnected from web socket")
                break
            await asyncio.sleep(20)

        self.stats.CONNECTED = False
        logging.debug("debug: heartbeat has stopped")

    async def send(self, message):
        
        await self.ws.send(json.dumps(message))
        while True:
            recv_msg = await self.msg_queue.get()
            self.msg_queue.task_done()
            return ServerResponse(recv_msg, self)

    def __str__(self):
        return f"{self.url.scheme}://{self.url.hostname}:{self.url.port}"
    
    def __repr__(self):
        return f"<WSS '{self.alias}' ({self.url.scheme}://{self.url.username}@{self.url.hostname}:{self.url.port})>"
