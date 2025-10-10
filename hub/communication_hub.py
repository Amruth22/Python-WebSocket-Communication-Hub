"""
Communication Hub
Central hub for real-time communication
"""

import logging

logger = logging.getLogger(__name__)


class CommunicationHub:
    """
    Central communication hub
    Routes messages between clients
    """
    
    def __init__(self, socketio, connection_manager, room_manager, message_store):
        """
        Initialize communication hub
        
        Args:
            socketio: SocketIO instance
            connection_manager: ConnectionManager instance
            room_manager: RoomManager instance
            message_store: MessageStore instance
        """
        self.socketio = socketio
        self.connection_manager = connection_manager
        self.room_manager = room_manager
        self.message_store = message_store
        
        logger.info("Communication Hub initialized")
    
    def send_to_user(self, user_id, message):
        """
        Send message to a specific user
        
        Args:
            user_id: Target user ID
            message: Message to send
        """
        # Get user's connections
        connection_ids = self.connection_manager.get_user_connections(user_id)
        
        if connection_ids:
            # User is online, send immediately
            for conn_id in connection_ids:
                conn_info = self.connection_manager.get_connection(conn_id)
                if conn_info:
                    self.socketio.emit('message', message, room=conn_info['sid'])
            
            logger.debug(f"Message sent to user {user_id}")
        else:
            # User is offline, queue message
            self.message_store.save_message(
                sender_id=message.get('sender_id'),
                recipient_id=user_id,
                message_type='direct',
                content=message
            )
            
            logger.debug(f"Message queued for offline user {user_id}")
    
    def broadcast_all(self, message):
        """
        Broadcast message to all connected clients
        
        Args:
            message: Message to broadcast
        """
        self.socketio.emit('broadcast', message)
        logger.info("Message broadcasted to all clients")
    
    def send_to_room(self, room_id, message):
        """
        Send message to a room
        
        Args:
            room_id: Room ID
            message: Message to send
        """
        self.socketio.emit('room_message', message, room=room_id)
        
        # Also save to database
        self.message_store.save_message(
            sender_id=message.get('sender_id'),
            room_id=room_id,
            message_type='room',
            content=message
        )
        
        logger.debug(f"Message sent to room {room_id}")
    
    def deliver_queued_messages(self, user_id):
        """
        Deliver queued messages to user when they come online
        
        Args:
            user_id: User ID
        """
        # Get undelivered messages
        messages = self.message_store.get_undelivered_messages(user_id)
        
        if messages:
            logger.info(f"Delivering {len(messages)} queued messages to user {user_id}")
            
            for msg in messages:
                self.send_to_user(user_id, msg['content'])
                self.message_store.mark_delivered(msg['id'])
