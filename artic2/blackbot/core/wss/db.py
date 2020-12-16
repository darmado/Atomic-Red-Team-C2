import aiosqlite
import sqlite3
import logging
import asyncio
import uuid
from blackbot.core.utils import get_path_in_artic2

class AsyncARTIC2db:

    def __init__(self, db_path=get_path_in_artic2("artic2.db")):
        self.db_path = db_path

    @staticmethod
    async def create_db_and_schema(db_path=get_path_in_artic2("artic2.db")):
        with sqlite3.connect(db_path) as db:
            db.execute('''CREATE TABLE "sessions" (
                            "id" integer PRIMARY KEY,
                            "guid" text,
                            "psk" text,
                            "location" text,
                            UNIQUE(guid,psk)
                        )''')

    def add_session(self, guid, psk: str):
        with self.db:
            try:
                self.db.execute("INSERT INTO sessions (guid, psk) VALUES (?,?)", [str(guid), psk])
                return psk
            except sqlite3.IntegrityError:
                logging.debug(f"Session with guid {guid} already present in database")

    def add_location(self, guid, location):
        with self.db:
            try:
                self.db.execute(f"UPDATE sessions SET location = '{location}' WHERE guid = '{guid}'")

            except sqlite3.IntegrityError:
                logging.debug(f"Session with guid {guid} not present in database")

    def remove_session(self, guid):
        with self.db:
            try:
                self.db.execute(f"DELETE FROM sessions WHERE guid = '{guid}'")
                return
            except sqlite3.IntegrityError:
                logging.debug(f"Could not remove {guid} from the database")

    def get_session_psk(self, guid):
        with self.db:
            query = self.db.execute("SELECT psk FROM sessions WHERE guid=(?)", [str(guid)])
            result = query.fetchone()
            return result[0] if result else None
    
    def get_session_location(self, guid):
        with self.db:
            query = self.db.execute("SELECT location FROM sessions WHERE guid=(?)", [str(guid)])
            result = query.fetchone()
            return result[0] if result else None

    def get_sessions(self):
        with self.db:
            query = self.db.execute("SELECT * FROM sessions")
            return query.fetchall()

    def __enter__(self):
        self.db = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exec_type, exc, tb):
        self.db.close()
