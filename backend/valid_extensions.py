
print("Testing Extension Imports...")
try:
    print("Importing SQLAlchemy...")
    from flask_sqlalchemy import SQLAlchemy
    print("OK SQLAlchemy")
except: print("FAIL SQLAlchemy")

try:
    print("Importing Migrate...")
    from flask_migrate import Migrate
    print("OK Migrate")
except: print("FAIL Migrate")

try:
    print("Importing JWT...")
    from flask_jwt_extended import JWTManager
    print("OK JWT")
except: print("FAIL JWT")

try:
    print("Importing Cache...")
    from flask_caching import Cache
    print("OK Cache")
except: print("FAIL Cache")

try:
    print("Importing Limiter...")
    from flask_limiter import Limiter
    print("OK Limiter")
except: print("FAIL Limiter")

try:
    print("Importing SocketIO...")
    from flask_socketio import SocketIO
    print("OK SocketIO")
except: print("FAIL SocketIO")
