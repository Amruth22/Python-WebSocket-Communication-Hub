"""
Connection Pool
Manages WebSocket connection pooling
"""

import logging

logger = logging.getLogger(__name__)


class ConnectionPool:
    """
    WebSocket connection pool
    Manages connection limits and pooling
    """
    
    def __init__(self, max_connections_per_user=5):
        """
        Initialize connection pool
        
        Args:
            max_connections_per_user: Maximum connections per user
        """
        self.max_connections_per_user = max_connections_per_user
        self.user_connections = {}  # {user_id: [connection_ids]}
        
        logger.info(f"Connection Pool initialized (max per user: {max_connections_per_user})")
    
    def can_add_connection(self, user_id):
        """
        Check if user can add another connection
        
        Args:
            user_id: User ID
            
        Returns:
            True if allowed, False if limit reached
        """
        if user_id not in self.user_connections:
            return True
        
        return len(self.user_connections[user_id]) < self.max_connections_per_user
    
    def add_connection(self, user_id, connection_id):
        """
        Add connection to pool
        
        Args:
            user_id: User ID
            connection_id: Connection ID
            
        Returns:
            True if added, False if limit reached
        """
        if not self.can_add_connection(user_id):
            logger.warning(f"Connection limit reached for user {user_id}")
            return False
        
        if user_id not in self.user_connections:
            self.user_connections[user_id] = []
        
        self.user_connections[user_id].append(connection_id)
        
        logger.info(f"Connection added to pool: {connection_id} for user {user_id}")
        return True
    
    def remove_connection(self, user_id, connection_id):
        """
        Remove connection from pool
        
        Args:
            user_id: User ID
            connection_id: Connection ID
        """
        if user_id in self.user_connections:
            if connection_id in self.user_connections[user_id]:
                self.user_connections[user_id].remove(connection_id)
                
                # Clean up empty list
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]
                
                logger.info(f"Connection removed from pool: {connection_id}")
    
    def get_user_connection_count(self, user_id):
        """Get number of connections for a user"""
        return len(self.user_connections.get(user_id, []))
    
    def get_stats(self):
        """Get pool statistics"""
        total_connections = sum(len(conns) for conns in self.user_connections.values())
        
        return {
            'total_connections': total_connections,
            'users_with_connections': len(self.user_connections),
            'max_per_user': self.max_connections_per_user,
            'avg_connections_per_user': total_connections / len(self.user_connections) if self.user_connections else 0
        }
