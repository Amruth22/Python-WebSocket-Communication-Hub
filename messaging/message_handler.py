"""
Message Handler
Handles message processing and validation
"""

import logging
import time

logger = logging.getLogger(__name__)


class MessageHandler:
    """
    Message processing and validation
    """
    
    def __init__(self):
        """Initialize message handler"""
        self.message_count = 0
        logger.info("Message Handler initialized")
    
    def process_message(self, message, sender_id):
        """
        Process incoming message
        
        Args:
            message: Message dictionary
            sender_id: Sender user ID
            
        Returns:
            Processed message
        """
        self.message_count += 1
        
        # Add metadata
        processed = {
            'id': self.message_count,
            'sender_id': sender_id,
            'content': message.get('content', ''),
            'type': message.get('type', 'text'),
            'timestamp': time.time()
        }
        
        # Add recipient info if present
        if 'recipient_id' in message:
            processed['recipient_id'] = message['recipient_id']
        
        if 'room_id' in message:
            processed['room_id'] = message['room_id']
        
        logger.debug(f"Message processed: {processed['id']}")
        
        return processed
    
    def validate_message(self, message):
        """
        Validate message format
        
        Args:
            message: Message to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        if not isinstance(message, dict):
            return False
        
        if 'content' not in message:
            return False
        
        # Check message type
        valid_types = ['text', 'image', 'file', 'notification']
        if message.get('type') and message['type'] not in valid_types:
            return False
        
        return True
    
    def sanitize_message(self, message):
        """
        Sanitize message content
        
        Args:
            message: Message to sanitize
            
        Returns:
            Sanitized message
        """
        if isinstance(message.get('content'), str):
            # Remove potentially dangerous content
            sanitized_content = message['content'].replace('<script>', '').replace('</script>', '')
            message['content'] = sanitized_content
        
        return message
