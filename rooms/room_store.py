"""
Room Store
SQLite storage for rooms
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)


class RoomStore:
    """
    SQLite-based room storage
    """
    
    def __init__(self, db_path='websocket.db'):
        """
        Initialize room store
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("Room Store initialized")
    
    def save_room(self, room_id, room_name, created_by, is_private=False):
        """
        Save room to database
        
        Args:
            room_id: Room ID
            room_name: Room name
            created_by: Creator user ID
            is_private: Whether room is private
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO rooms (room_id, room_name, created_by, is_private)
            VALUES (?, ?, ?, ?)
        ''', (room_id, room_name, created_by, is_private))
        
        conn.commit()
        conn.close()
    
    def delete_room(self, room_id):
        """
        Delete room
        
        Args:
            room_id: Room ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Delete room members
        cursor.execute('DELETE FROM room_members WHERE room_id = ?', (room_id,))
        
        # Delete room
        cursor.execute('DELETE FROM rooms WHERE room_id = ?', (room_id,))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Room deleted: {room_id}")
    
    def get_room(self, room_id):
        """
        Get room from database
        
        Args:
            room_id: Room ID
            
        Returns:
            Room dictionary or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM rooms WHERE room_id = ?', (room_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return dict(row)
        
        return None
