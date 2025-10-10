"""
Connection Manager
Manages WebSocket connections
"""

import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    WebSocket connection manager
    Tracks all active WebSocket connections
    """
    
    def __init__(self):
        """Initialize connection manager"""
        self.connections = {}  # {connection_id: connection_info}
        self.user_connections = {}  # {user_id: [connection_ids]}
        
        logger.info("Connection Manager initialized")
    
    def add_connection(self, connection_id, user_id, sid):
        """
        Add a WebSocket connection
        
        Args:
            connection_id: Unique connection ID
            user_id: User ID
            sid: Socket.IO session ID
        """
        connection_info = {
            'connection_id': connection_id,
            'user_id': user_id,
            'sid': sid,
            'connected_at': time.time(),
            'last_activity': time.time()
        }
        
        self.connections[connection_id] = connection_info
        
        # Track user connections
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        
        self.user_connections[user_id].append(connection_id)
        
        logger.info(f"Connection added: {connection_id} for user {user_id}")
    
    def remove_connection(self, connection_id):
        """
        Remove a WebSocket connection
        
        Args:
            connection_id: Connection ID to remove
        """
        if connection_id in self.connections:
            connection_info = self.connections[connection_id]
            user_id = connection_info['user_id']
            
            # Remove from connections
            del self.connections[connection_id]
            
            # Remove from user connections
            if user_id in self.user_connections:
                self.user_connections[user_id].remove(connection_id)
                
                # Clean up empty list
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]
            
            logger.info(f"Connection removed: {connection_id}")
    
    def get_connection(self, connection_id):
        """Get connection info by ID"""
        return self.connections.get(connection_id)
    
    def get_user_connections(self, user_id):
        """
        Get all connections for a user
        
        Args:
            user_id: User ID
            
        Returns:
            List of connection IDs
        """
        return self.user_connections.get(user_id, [])
    
    def is_user_online(self, user_id):
        """
        Check if user has any active connections
        
        Args:
            user_id: User ID
            
        Returns:
            True if online, False otherwise
        """
        return user_id in self.user_connections and len(self.user_connections[user_id]) > 0
    
    def get_online_users(self):
        """Get list of online user IDs"""
        return list(self.user_connections.keys())
    
    def update_activity(self, connection_id):
        """
        Update last activity timestamp
        
        Args:
            connection_id: Connection ID
        """
        if connection_id in self.connections:
            self.connections[connection_id]['last_activity'] = time.time()
    
    def get_stats(self):
        """Get connection statistics"""
        return {
            'total_connections': len(self.connections),
            'online_users': len(self.user_connections),
            'connections_by_user': {
                user_id: len(conn_ids) 
                for user_id, conn_ids in self.user_connections.items()
            }
        }
