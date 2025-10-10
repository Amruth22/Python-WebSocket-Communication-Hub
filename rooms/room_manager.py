"""
Room Manager
Manages chat rooms with SQLite storage
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)


class RoomManager:
    """
    Room manager with SQLite storage
    """
    
    def __init__(self, db_path='websocket.db'):
        """
        Initialize room manager
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("Room Manager initialized")
    
    def create_room(self, room_id, room_name, created_by, is_private=False, max_members=100):
        """
        Create a new room
        
        Args:
            room_id: Unique room ID
            room_name: Room name
            created_by: User ID who created room
            is_private: Whether room is private
            max_members: Maximum members allowed
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO rooms (room_id, room_name, created_by, is_private, max_members)
                VALUES (?, ?, ?, ?, ?)
            ''', (room_id, room_name, created_by, is_private, max_members))
            
            conn.commit()
            logger.info(f"Room created: {room_id} ({room_name})")
        except sqlite3.IntegrityError:
            logger.warning(f"Room already exists: {room_id}")
        finally:
            conn.close()
    
    def join_room(self, room_id, user_id):
        """
        Add user to room
        
        Args:
            room_id: Room ID
            user_id: User ID
            
        Returns:
            True if joined, False if failed
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if room exists
        cursor.execute('SELECT max_members FROM rooms WHERE room_id = ?', (room_id,))
        room = cursor.fetchone()
        
        if not room:
            conn.close()
            logger.warning(f"Room not found: {room_id}")
            return False
        
        max_members = room[0]
        
        # Check current member count
        cursor.execute('SELECT COUNT(*) FROM room_members WHERE room_id = ?', (room_id,))
        current_count = cursor.fetchone()[0]
        
        if current_count >= max_members:
            conn.close()
            logger.warning(f"Room full: {room_id}")
            return False
        
        # Add user to room
        try:
            cursor.execute('''
                INSERT INTO room_members (room_id, user_id)
                VALUES (?, ?)
            ''', (room_id, user_id))
            
            conn.commit()
            logger.info(f"User {user_id} joined room {room_id}")
            return True
        except sqlite3.IntegrityError:
            logger.debug(f"User {user_id} already in room {room_id}")
            return True
        finally:
            conn.close()
    
    def leave_room(self, room_id, user_id):
        """
        Remove user from room
        
        Args:
            room_id: Room ID
            user_id: User ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DELETE FROM room_members 
            WHERE room_id = ? AND user_id = ?
        ''', (room_id, user_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"User {user_id} left room {room_id}")
    
    def get_room_members(self, room_id):
        """
        Get all members of a room
        
        Args:
            room_id: Room ID
            
        Returns:
            List of user IDs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id FROM room_members WHERE room_id = ?', (room_id,))
        rows = cursor.fetchall()
        
        conn.close()
        
        return [row[0] for row in rows]
    
    def get_user_rooms(self, user_id):
        """
        Get all rooms a user is in
        
        Args:
            user_id: User ID
            
        Returns:
            List of room IDs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT room_id FROM room_members WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        
        conn.close()
        
        return [row[0] for row in rows]
    
    def get_room_info(self, room_id):
        """
        Get room information
        
        Args:
            room_id: Room ID
            
        Returns:
            Room info dictionary
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM rooms WHERE room_id = ?', (room_id,))
        row = cursor.fetchone()
        
        if row:
            # Get member count
            cursor.execute('SELECT COUNT(*) FROM room_members WHERE room_id = ?', (room_id,))
            member_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'room_id': row['room_id'],
                'room_name': row['room_name'],
                'created_by': row['created_by'],
                'is_private': bool(row['is_private']),
                'max_members': row['max_members'],
                'member_count': member_count
            }
        
        conn.close()
        return None
    
    def list_rooms(self):
        """
        List all rooms
        
        Returns:
            List of room info
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT room_id FROM rooms')
        rows = cursor.fetchall()
        
        conn.close()
        
        rooms = []
        for row in rows:
            room_info = self.get_room_info(row['room_id'])
            if room_info:
                rooms.append(room_info)
        
        return rooms
