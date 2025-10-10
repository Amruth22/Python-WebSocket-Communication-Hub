"""
Offline Queue
SQLite-based offline message queue
"""

import sqlite3
import json
import logging

logger = logging.getLogger(__name__)


class OfflineQueue:
    """
    Offline message queue with SQLite
    Stores messages for offline users
    """
    
    def __init__(self, db_path='websocket.db', max_messages=100):
        """
        Initialize offline queue
        
        Args:
            db_path: Path to SQLite database
            max_messages: Maximum messages per user
        """
        self.db_path = db_path
        self.max_messages = max_messages
        
        logger.info(f"Offline Queue initialized (max: {max_messages})")
    
    def add_message(self, user_id, message, sender_id=None):
        """
        Add message to offline queue
        
        Args:
            user_id: Recipient user ID
            message: Message content
            sender_id: Sender user ID
            
        Returns:
            Message ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check queue size
        cursor.execute('''
            SELECT COUNT(*) FROM messages 
            WHERE recipient_id = ? AND delivered = 0
        ''', (user_id,))
        
        count = cursor.fetchone()[0]
        
        if count >= self.max_messages:
            # Delete oldest message
            cursor.execute('''
                DELETE FROM messages 
                WHERE id = (
                    SELECT id FROM messages 
                    WHERE recipient_id = ? AND delivered = 0 
                    ORDER BY created_at ASC 
                    LIMIT 1
                )
            ''', (user_id,))
        
        # Add message
        content_json = json.dumps(message)
        
        cursor.execute('''
            INSERT INTO messages (sender_id, recipient_id, message_type, content, delivered)
            VALUES (?, ?, ?, ?, 0)
        ''', (sender_id, user_id, 'offline', content_json))
        
        message_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        logger.info(f"Message queued for offline user {user_id}")
        
        return message_id
    
    def get_messages(self, user_id):
        """
        Get all queued messages for user
        
        Args:
            user_id: User ID
            
        Returns:
            List of messages
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM messages 
            WHERE recipient_id = ? AND delivered = 0 
            ORDER BY created_at ASC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        messages = []
        for row in rows:
            messages.append({
                'id': row['id'],
                'sender_id': row['sender_id'],
                'content': json.loads(row['content']) if row['content'] else {},
                'created_at': row['created_at']
            })
        
        return messages
    
    def mark_delivered(self, message_id):
        """
        Mark message as delivered
        
        Args:
            message_id: Message ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE messages 
            SET delivered = 1, delivered_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (message_id,))
        
        conn.commit()
        conn.close()
    
    def get_queue_size(self, user_id):
        """
        Get number of queued messages
        
        Args:
            user_id: User ID
            
        Returns:
            Message count
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM messages 
            WHERE recipient_id = ? AND delivered = 0
        ''', (user_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
