import os
import html
import time

from dotenv import load_dotenv

from flask import request
from flask_socketio import SocketIO

load_dotenv()


class SocketManager:
    def __init__(self, app, ratelimit, log, db_query):
        self.app = app
        self.socketio = SocketIO(app, async_mode='gevent',
                                 cors_allowed_origins=['http://[::1]:7654', 'http://hermes.i2p'])

        self.ratelimit = ratelimit
        self.log = log
        self.db_query = db_query

        self.socketio.on_event('message', self.handle_message)
        self.socketio.on_event('connect', self.handle_connect)
        self.socketio.on_event('disconnect', self.handle_disconnect)

    def run(self):
        host = os.getenv('HOST')
        port = int(os.getenv('MAIN_PORT'))
        self.socketio.run(self.app, host=host, port=port, use_reloader=True)

    def handle_connect(self):
        print("Client connected")
        self.socketio.send('--- Client connected ---')

    def handle_message(self, message):
        token = request.cookies.get('token')
        if not token:
            return
        limit = self.ratelimit(token)
        if limit:
            self.log(token, message, time.time(), limit)
            return

        msg_content = message.get('message')
        if msg_content:
            self.log(token, msg_content, time.time())
            if len(msg_content) > int(os.getenv('MESSAGE_SIZE')):
                return
            message = html.escape(msg_content)
            self.db_query("INSERT INTO messages (token, message, timestamp) VALUES (?, ?, ?)",
                          (token, message, time.time()))

            self.socketio.emit('message', message)

    def handle_disconnect(self):
        self.socketio.send('--- Client disconnected ---')
