import os

import sqlite3
from flask import g


class DataControl:

    def __init__(self):
        self.messages_path = os.getenv('MESSAGES_DB')

    def get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self.messages_path)
        return db

    def query_db(self, query, args=(), one=False):
        db = self.get_db()
        cur = db.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        db.commit()
        return (rv[0] if rv else None) if one else rv
