"""
Flask-SocketIO Application
WebSocket communication hub with real-time messaging
"""

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging
import os
import uuid

from storage.database import init_database
from storage.message_store import MessageStore
from websocket.connection_manager import ConnectionManager
from websocket.connection_pool import ConnectionPool
from websocket.connection_state import ConnectionState
from hub.communication_hub import CommunicationHub
from hub.broadcast_manager import BroadcastManager
from rooms.room_manager import RoomManager
from messaging.offline_queue import OfflineQueue
from messaging.message_handler import MessageHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-change-in-production'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize database
db_path = os.getenv('DATABASE_PATH', 'websocket.db')
init_database(db_path)

# Initialize components
connection_manager = ConnectionManager()
connection_pool = ConnectionPool(max_connections_per_user=5)
connection_state = ConnectionState(db_path)
message_store = MessageStore(db_path)
room_manager = RoomManager(db_path)
offline_queue = OfflineQueue(db_path)
message_handler = MessageHandler()
broadcast_manager = BroadcastManager(socketio, connection_manager)
communication_hub = CommunicationHub(socketio, connection_manager, room_manager, message_store)


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'WebSocket Communication Hub',
        'version': '1.0.0',
        'features': [
            'Real-time messaging',
            'Room-based chat',
            'Offline message queue',
            'Connection state tracking',
            'Message broadcasting'
        ],
        'websocket_endpoint': '/socket.io'
    })


@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'healthy'})


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    conn_stats = connection_manager.get_stats()
    pool_stats = connection_pool.get_stats()
    
    return jsonify({
        'connections': conn_stats,
        'pool': pool_stats,
        'online_users': connection_state.get_online_users()
    })


@app.route('/api/rooms', methods=['GET'])
def list_rooms():
    """List all rooms"""
    rooms = room_manager.list_rooms()
    
    return jsonify({
        'rooms': rooms,
        'count': len(rooms)
    })


@app.route('/api/rooms/<room_id>', methods=['GET'])
def get_room(room_id):
    """Get room information"""
    room_info = room_manager.get_room_info(room_id)
    
    if room_info:
        return jsonify(room_info)
    else:
        return jsonify({'error': 'Room not found'}), 404


# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    
    emit('connected', {'message': 'Connected to WebSocket server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")
    
    # Find and remove connection
    for conn_id, conn_info in list(connection_manager.connections.items()):
        if conn_info['sid'] == request.sid:
            user_id = conn_info['user_id']
            
            connection_manager.remove_connection(conn_id)
            connection_pool.remove_connection(user_id, conn_id)
            
            # Update state if no more connections
            if not connection_manager.is_user_online(user_id):
                connection_state.set_state(user_id, ConnectionState.STATE_OFFLINE)
            
            break


@socketio.on('register')
def handle_register(data):
    """Register user connection"""
    user_id = data.get('user_id')
    
    if not user_id:
        emit('error', {'message': 'user_id required'})
        return
    
    # Check connection limit
    if not connection_pool.can_add_connection(user_id):
        emit('error', {'message': 'Connection limit reached'})
        return
    
    # Create connection
    connection_id = str(uuid.uuid4())
    connection_manager.add_connection(connection_id, user_id, request.sid)
    connection_pool.add_connection(user_id, connection_id)
    
    # Set state to online
    connection_state.set_state(user_id, ConnectionState.STATE_ONLINE)
    
    # Deliver queued messages
    communication_hub.deliver_queued_messages(user_id)
    
    emit('registered', {
        'connection_id': connection_id,
        'user_id': user_id,
        'message': 'Registered successfully'
    })
    
    logger.info(f"User registered: {user_id} with connection {connection_id}")


@socketio.on('message')
def handle_message(data):
    """Handle incoming message"""
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    content = data.get('content')
    
    if not sender_id or not content:
        emit('error', {'message': 'sender_id and content required'})
        return
    
    # Process message
    message = message_handler.process_message(data, sender_id)
    
    # Send to recipient
    if recipient_id:
        communication_hub.send_to_user(recipient_id, message)
    
    emit('message_sent', {'status': 'success', 'message_id': message['id']})


@socketio.on('join_room')
def handle_join_room(data):
    """Handle join room request"""
    room_id = data.get('room_id')
    user_id = data.get('user_id')
    
    if not room_id or not user_id:
        emit('error', {'message': 'room_id and user_id required'})
        return
    
    # Join room in database
    success = room_manager.join_room(room_id, user_id)
    
    if success:
        # Join Socket.IO room
        join_room(room_id)
        
        emit('joined_room', {
            'room_id': room_id,
            'message': f'Joined room {room_id}'
        })
        
        # Notify room
        emit('user_joined', {
            'user_id': user_id,
            'room_id': room_id
        }, room=room_id, skip_sid=request.sid)
    else:
        emit('error', {'message': 'Failed to join room'})


@socketio.on('leave_room')
def handle_leave_room(data):
    """Handle leave room request"""
    room_id = data.get('room_id')
    user_id = data.get('user_id')
    
    if not room_id or not user_id:
        emit('error', {'message': 'room_id and user_id required'})
        return
    
    # Leave room in database
    room_manager.leave_room(room_id, user_id)
    
    # Leave Socket.IO room
    leave_room(room_id)
    
    emit('left_room', {
        'room_id': room_id,
        'message': f'Left room {room_id}'
    })
    
    # Notify room
    emit('user_left', {
        'user_id': user_id,
        'room_id': room_id
    }, room=room_id)


@socketio.on('room_message')
def handle_room_message(data):
    """Handle room message"""
    room_id = data.get('room_id')
    sender_id = data.get('sender_id')
    content = data.get('content')
    
    if not room_id or not sender_id or not content:
        emit('error', {'message': 'room_id, sender_id, and content required'})
        return
    
    # Process message
    message = message_handler.process_message(data, sender_id)
    
    # Send to room
    communication_hub.send_to_room(room_id, message)
    
    emit('message_sent', {'status': 'success'})


@socketio.on('broadcast')
def handle_broadcast(data):
    """Handle broadcast message"""
    sender_id = data.get('sender_id')
    content = data.get('content')
    
    if not sender_id or not content:
        emit('error', {'message': 'sender_id and content required'})
        return
    
    # Process message
    message = message_handler.process_message(data, sender_id)
    
    # Broadcast to all
    communication_hub.broadcast_all(message)
    
    emit('broadcast_sent', {'status': 'success'})


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print("=" * 60)
    print("WebSocket Communication Hub")
    print("=" * 60)
    print(f"Starting on port {port}")
    print("Features:")
    print("  - Real-time messaging")
    print("  - Room-based communication")
    print("  - Offline message queue")
    print("  - Connection state tracking")
    print("  - Message broadcasting")
    print("=" * 60)
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)
