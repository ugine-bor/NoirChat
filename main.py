from gevent import monkey

monkey.patch_all()

import json
import os
import time

from flask import Flask, render_template, make_response, url_for, request, g, abort

from dotenv import load_dotenv
import secrets

import atexit

from scripts.data_control import DataControl
from scripts.websocket_handlers import SocketManager
from scripts.redis_control import RedisManager
from scripts.logs import LogManager
from scripts.token_tweaks import generate_signed_token, verify_token

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('KEY')

############

Redis = RedisManager()
Log = LogManager()
Data = DataControl()
Websocket = SocketManager(app, Redis.ratelimit, Log.log, Data.query_db)


############

@app.errorhandler(500)
def internal_server_error(e):
    return f"<link rel='stylesheet' href={url_for('static', filename='css/error.css')}> " \
           "Shit happens", 500


@app.errorhandler(403)
def forbidden(e):
    return f"Shit happens", 403


@app.route('/')
def index():
    nonce = secrets.token_urlsafe(16)
    msgs = Data.query_db("SELECT message FROM messages ORDER BY timestamp ASC LIMIT 100")
    resp = make_response(
        render_template('main.html', nonce=nonce, message_size=int(os.getenv('MESSAGE_SIZE')), messages=msgs))

    csp = f"default-src 'self'; img-src 'self' data:; script-src 'self' 'nonce-{nonce}'; style-src 'self'; object-src 'none'; media-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self';"
    resp.headers['Content-Security-Policy'] = csp
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'DENY'

    return resp


@app.route('/chat')
def chat():
    token = request.cookies.get('token')
    if not token or not verify_token(token, app):
        token = generate_signed_token(app)
        data = {'last': time.time(), 'count': 1}
        Redis.ratelimits.set(token, json.dumps(data), ex=int(os.getenv('MESSAGE_EXPIRE')))
    else:
        data = Redis.ratelimits.get(token)
        if data:
            data = json.loads(data.decode('utf-8'))
            data['count'] += 1
            data['last'] = time.time()
        else:
            data = {'last': time.time(), 'count': 1}
        Redis.ratelimits.set(token, json.dumps(data), ex=int(os.getenv('MESSAGE_EXPIRE')))

    nonce = secrets.token_urlsafe(16)
    msgs = Data.query_db("SELECT message FROM messages ORDER BY timestamp ASC LIMIT 100")
    resp = make_response(
        render_template('chat.html', nonce=nonce, message_size=int(os.getenv('MESSAGE_SIZE')), messages=msgs))
    resp.set_cookie('token', token, max_age=int(os.getenv('COOKIE_LIFE')), httponly=True, samesite='Lax')

    csp = f"default-src 'self'; img-src 'self' data:; script-src 'self' 'nonce-{nonce}'; style-src 'self'; object-src 'none'; media-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self';"
    resp.headers['Content-Security-Policy'] = csp
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'DENY'

    return resp


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
    print("Database closed.")


@atexit.register
def cleanup():
    Redis.disconnect()
    print("Redis stopped.")


if __name__ == '__main__':
    load_dotenv()
    Redis.run()
    Websocket.run()
