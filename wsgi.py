from dotenv import load_dotenv
load_dotenv()

# Crucially, ensure main.py runs gevent.monkey.patch_all() *first*
from main import app , Websocket
from werkzeug.middleware.proxy_fix import ProxyFix

# Get a reference to the socketio instance
# This assumes 'Websocket' is your initialized SocketManager instance
socketio = Websocket.socketio
raw_app = socketio.wsgi_app if hasattr(socketio, 'wsgi_app') else app

# Wrap the app, telling it to trust 1 level of proxy (i2pd) for specific headers
# Adjust counts (e.g., x_for=1) if i2pd adds multiple headers or you have more layers
application = ProxyFix(raw_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# This is the WSGI application callable that Gunicorn will use
# Your original logic here is likely correct for Flask-SocketIO with Gunicorn
#application = socketio.wsgi_app if hasattr(socketio, 'wsgi_app') else app
#application = app
