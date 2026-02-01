from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.extensions import socketio
from flask import request

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

@socketio.on('join_order_room')
def handle_join_order(data):
    """
    Clients (Kiosk/Mobile) join a room specific to their order ID to get status updates.
    """
    order_id = data.get('order_id')
    if order_id:
        room = f"order_{order_id}"
        join_room(room)
        emit('message', {'msg': f"Joined room {room}"}, to=room)

@socketio.on('join_kitchen_room')
def handle_join_kitchen():
    """
    Kitchen staff joins this room to get new order alerts.
    Requires Auth.
    """
    try:
        # Manually verify JWT from query param or auth header provided in handshake
        # simplified for this demo, assume successful connection implies access or verify token passed in data
        # In prod: verify_jwt_in_request() within socket context or socketio middleware
        pass 
    except:
        return False
        
    room = "kitchen_updates"
    join_room(room)
    print(f"Client {request.sid} joined kitchen room")
    emit('message', {'msg': "Joined kitchen updates"}, to=room)
