"""
Message Router
Routes messages to appropriate destinations
"""

import logging

logger = logging.getLogger(__name__)


class MessageRouter:
    """
    Routes messages based on type and destination
    """
    
    def __init__(self, communication_hub):
        """
        Initialize message router
        
        Args:
            communication_hub: CommunicationHub instance
        """
        self.hub = communication_hub
        logger.info("Message Router initialized")
    
    def route_message(self, message):
        """
        Route message to appropriate destination
        
        Args:
            message: Message dictionary with routing info
        """
        message_type = message.get('type')
        
        if message_type == 'direct':
            # Direct message to user
            recipient_id = message.get('recipient_id')
            if recipient_id:
                self.hub.send_to_user(recipient_id, message)
        
        elif message_type == 'room':
            # Room message
            room_id = message.get('room_id')
            if room_id:
                self.hub.send_to_room(room_id, message)
        
        elif message_type == 'broadcast':
            # Broadcast to all
            self.hub.broadcast_all(message)
        
        else:
            logger.warning(f"Unknown message type: {message_type}")
