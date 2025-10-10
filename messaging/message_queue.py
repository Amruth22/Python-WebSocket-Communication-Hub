"""
Message Queue
In-memory message queuing
"""

import logging
from collections import defaultdict, deque

logger = logging.getLogger(__name__)


class MessageQueue:
    """
    In-memory message queue
    """
    
    def __init__(self, max_size=100):
        """
        Initialize message queue
        
        Args:
            max_size: Maximum messages per user
        """
        self.max_size = max_size
        self.queues = defaultdict(lambda: deque(maxlen=max_size))
        
        logger.info(f"Message Queue initialized (max size: {max_size})")
    
    def enqueue(self, user_id, message):
        """
        Add message to queue
        
        Args:
            user_id: User ID
            message: Message to queue
        """
        self.queues[user_id].append(message)
        logger.debug(f"Message queued for user {user_id}")
    
    def dequeue(self, user_id):
        """
        Get next message from queue
        
        Args:
            user_id: User ID
            
        Returns:
            Message or None
        """
        if self.queues[user_id]:
            return self.queues[user_id].popleft()
        return None
    
    def dequeue_all(self, user_id):
        """
        Get all messages from queue
        
        Args:
            user_id: User ID
            
        Returns:
            List of messages
        """
        messages = list(self.queues[user_id])
        self.queues[user_id].clear()
        return messages
    
    def get_queue_size(self, user_id):
        """Get number of queued messages for user"""
        return len(self.queues[user_id])
    
    def clear_queue(self, user_id):
        """Clear queue for user"""
        self.queues[user_id].clear()
