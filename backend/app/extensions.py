from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


print("Importing Extensions...")
print("Imp JWT")
from flask_jwt_extended import JWTManager
from flask_caching import Cache
print("Imp Limiter")
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
print("Skipping SocketIO Import due to crash")
# from flask_socketio import SocketIO
socketio = None



db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)

# Force threading mode to avoid eventlet crashes on Python 3.14
# socketio = SocketIO(async_mode='threading')
socketio = None # Disabled due to crash


