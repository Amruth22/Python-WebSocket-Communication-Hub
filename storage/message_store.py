"""
Message Store
SQLite-based message persistence
"""

import sqlite3
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MessageStore:
    """
    SQLite-based message storage
    """
    
    def __init__(self, db_path='websocket.db'):
        """
        Initialize message store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("Message Store initialized")
    
    def save_message(self, sender_id, recipient_id=None, room_id=None, 
                    message_type='text', content=None):
        """
        Save a message
        
        Args:
            sender_id: Sender user ID
            recipient_id: Recipient user ID (for direct messages)
            room_id: Room ID (for room messages)
            message_type: Type of message
            content: Message content (dict)
            
        Returns:
            Message ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        content_json = json.dumps(content) if content else None
        
        cursor.execute('''
            INSERT INTO messages (sender_id, recipient_id, room_id, message_type, content, delivered)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sender_id, recipient_id, room_id, message_type, content_json, 0))
        
        message_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        logger.debug(f"Message saved: {message_id}")
        
        return message_id
    
    def get_undelivered_messages(self, user_id):
        """
        Get undelivered messages for a user
        
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
                'message_type': row['message_type'],
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
    
    def delete_old_messages(self, days=7):
        """
        Delete messages older than specified days
        
        Args:
            days: Number of days to retain
            
        Returns:
            Number of deleted messages
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM messages 
            WHERE datetime(created_at) < datetime('now', '-' || ? || ' days')
        ''', (days,))
        
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Deleted {deleted} old messages")
        
        return deleted
