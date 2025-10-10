"""
Broadcast Manager
Manages message broadcasting
"""

import logging

logger = logging.getLogger(__name__)


class BroadcastManager:
    """
    Manages message broadcasting
    """
    
    def __init__(self, socketio, connection_manager):
        """
        Initialize broadcast manager
        
        Args:
            socketio: SocketIO instance
            connection_manager: ConnectionManager instance
        """
        self.socketio = socketio
        self.connection_manager = connection_manager
        
        logger.info("Broadcast Manager initialized")
    
    def broadcast_to_all(self, message, exclude_user=None):
        """
        Broadcast to all connected clients
        
        Args:
            message: Message to broadcast
            exclude_user: Optional user ID to exclude
        """
        if exclude_user:
            # Broadcast to all except specific user
            for user_id in self.connection_manager.get_online_users():
                if user_id != exclude_user:
                    connection_ids = self.connection_manager.get_user_connections(user_id)
                    for conn_id in connection_ids:
                        conn_info = self.connection_manager.get_connection(conn_id)
                        if conn_info:
                            self.socketio.emit('broadcast', message, room=conn_info['sid'])
        else:
            # Broadcast to all
            self.socketio.emit('broadcast', message)
        
        logger.info(f"Broadcast sent to all users (exclude: {exclude_user})")
    
    def broadcast_to_users(self, user_ids, message):
        """
        Broadcast to specific users
        
        Args:
            user_ids: List of user IDs
            message: Message to send
        """
        for user_id in user_ids:
            connection_ids = self.connection_manager.get_user_connections(user_id)
            
            for conn_id in connection_ids:
                conn_info = self.connection_manager.get_connection(conn_id)
                if conn_info:
                    self.socketio.emit('message', message, room=conn_info['sid'])
        
        logger.info(f"Broadcast sent to {len(user_ids)} users")
