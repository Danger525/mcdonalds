
from flask import Flask
from flask_socketio import SocketIO
print("Imports done")
app = Flask(__name__)
# Force threading async_mode
socketio = SocketIO(app, async_mode='threading')

@app.route('/')
def home():
    return "Socket Server Works"

if __name__ == '__main__':
    print("Starting Socket server...")
    try:
        socketio.run(app, port=5002)
    except Exception as e:
        print(f"Error: {e}")
