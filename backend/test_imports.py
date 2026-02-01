
import sys
print(f"Python: {sys.version}")
try:
    import flask
    print("Flask imported")
    import flask_sqlalchemy
    print("SQLAlchemy imported")
    import eventlet
    print("Eventlet imported")
    from app import create_app
    print("App Factory imported")
except Exception as e:
    print(f"Error: {e}")
except ImportError as e:
    print(f"ImportError: {e}")
