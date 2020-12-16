import json
import os
import logging
import copy
import traceback
from blackbot.core.wss.job import Job
from base64 import b64encode
from time import time
from datetime import datetime
import json
import requests
import hashlib

class Jobs:
    def __init__(self, session):
        self.session = session
        self.jobs = []
        self.jobs.append(Job(command=('CheckIn', [])))
    
    def next_job(self):
        try:
            return list(filter(lambda job: job.status == 'initialized', self.jobs))[-1]
        except IndexError:
            logging.error(f"No jobs available")

    def get_by_id(self, job_id):
        try:
            return list(filter(lambda job: job.id == job_id, self.jobs))[0]
        except IndexError:
            logging.error(f"Job with id {job_id} not found")

    def get(self, job_id=None):
        job = self.next_job()
        if job:
            try:
                job_payload = job.payload()
                job.status = 'started'
                return self.session.crypto.encrypt(job_payload)
            except Exception as e:
                self.jobs.remove(job)
                logging.error(f"Error generating payload for module '{job.module.name}': {e}")
                traceback.print_exc()

    def add(self, job):
        job_copy = copy.deepcopy(job)
        self.jobs.insert(0, job_copy)
        if job.command:
            if len(job.command) == 2:
                arg = job.command[1]
            else:
                arg = 'n/a'
            event_log = {
                "msg":             "Tasked Command Job",
                "job_cmd":         job.command[0],
                "job_cmd_arg":     arg,
                "utc_timestamp":   datetime.utcfromtimestamp(int(time())).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "local_timestamp": datetime.fromtimestamp(int(time())).strftime('%Y-%m-%dT%H:%M:%SZ'),
            }
            self.session.logger.info(json.dumps(event_log))
        else:
            event_log = {
                "utc_timestamp":  datetime.utcfromtimestamp(int(time())).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "msg":               "Technique executed:",
                "controller":            f"{job.module.name}",
                "last_updated_by":            job.module.last_updated_by            if 'last_updated_by'            in dir(job.module) else 'n/a',
                "ttp_id":       job.module.external_id           if 'options'           in dir(job.module) else 'n/a',
                "ttp_opts":       job.module.options           if 'options'           in dir(job.module) else 'n/a',
                "decompressed_file": job.module.decompressed_file if 'decompressed_file' in dir(job.module) else 'n/a',
                "file_name":         job.module.fname             if 'fname'             in dir(job.module) else 'n/a',
                "gzip_file":         job.module.gzip_file         if 'gzip_file'         in dir(job.module) else 'n/a',
                "language":          job.module.language          if 'language'          in dir(job.module) else 'n/a',
                "references":        job.module.references        if 'references'        in dir(job.module) else 'n/a',
                "run_in_thread":     job.module.run_in_thread     if 'run_in_thread'     in dir(job.module) else 'n/a',
                "job_id":       job.id, 
            }
            self.session.logger.info(f"{json.dumps(event_log)}")

    def decrypt(self, job_id, data):
        job = self.get_by_id(job_id)
        decrypted_job = json.loads(self.session.crypto.decrypt(data))
        output = decrypted_job['result']
        if job.module:
            if hasattr(job.module, 'process') and not decrypted_job['error'] == True:
                output = job.module.process(self, output)
                output = b64encode(json.dumps(output).encode()).decode()
                event_log = {
                    "utc_timestamp":   datetime.utcfromtimestamp(int(time())).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "session":           f"{self.session.guid}",
                    "msg":               f"Module {job.module.name} processed job results: {job_id}",
                    "module":            f"{job.module.name}",
                    "job_id":            f"{job_id}",
                    "evidence":          f"{output}",
                    "last_updated_by":            job.module.last_updated_by            if 'last_updated_by'            in dir(job.module) else 'n/a',
                    "ttp_id":     job.module.external_id,
                    "ttp_opts":       job.module.options           if 'options'           in dir(job.module) else 'n/a',
                    "decompressed_file": job.module.decompressed_file if 'decompressed_file' in dir(job.module) else 'n/a',
                    "file_name":         job.module.fname             if 'fname'             in dir(job.module) else 'n/a',
                    "gzip_file":         job.module.gzip_file         if 'gzip_file'         in dir(job.module) else 'n/a',
                    "language":          job.module.language          if 'language'          in dir(job.module) else 'n/a',
                    "references":        job.module.references        if 'references'        in dir(job.module) else 'n/a',
                    "run_in_thread":     job.module.run_in_thread     if 'run_in_thread'     in dir(job.module) else 'n/a',
                }
                self.session.logger.info(f"{json.dumps(event_log)}")
            else:
                output = b64encode(json.dumps(output).encode()).decode()
                if output[:8] == 'IkVycm9y':
                    status = '0'
                elif output[:11] == 'IlN5c3RlbS5':
                    status = '2'
                else:
                    status = '1'
                event_log = {
                    "utc_timestamp":   datetime.utcfromtimestamp(int(time())).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "session":         f"{self.session.guid}",
                    "job_id":     f"{job_id}",
                    "ttp_data":     job.module.external_id,
                    "evidence":        f"{output}",
                    "evidence_status": f"{status}",
                }
                self.session.logger.info(f"{json.dumps(event_log)}")

        elif job.command:
            event_log = {
                "utc_timestamp":   datetime.utcfromtimestamp(int(time())).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "session":         f"{self.session.guid}",
                "msg":             f"Session returned command: {job_id}",
                "job_id":          f"{job_id}",
                "evidence":        f"{output}",
            }
            self.session.logger.info(f"{json.dumps(event_log)}")

        return decrypted_job, output

    def __len__(self):
        return len(self.jobs)

    def __repr__(self):
        return f"<Jobs ({len(self.jobs)})>"
