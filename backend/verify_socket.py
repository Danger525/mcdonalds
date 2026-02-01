import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to WebSocket Server")

@sio.event
def disconnect():
    print("Disconnected from WebSocket Server")

@sio.event
def message(data):
    print(f"Received message: {data}")

@sio.event
def order_update(data):
    print(f"Received order_update: {data}")

@sio.event
def kitchen_update(data):
    print(f"Received kitchen_update: {data}")

def verify():
    # Attempt connection
    try:
        sio.connect('http://localhost:5000')
        
        # Test 1: Join Order Room
        print("Joining order room...")
        sio.emit('join_order_room', {'order_id': 1})
        time.sleep(1)
        
        # Test 2: Join Kitchen Room
        print("Joining kitchen room...")
        sio.emit('join_kitchen_room')
        time.sleep(1)
        
        print("Verification steps sent. Please manually trigger an update or check logs.")
        sio.disconnect()
        
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    verify()
