"""
Connection State
Manages connection state with SQLite
"""

import sqlite3
import logging
import time

logger = logging.getLogger(__name__)


class ConnectionState:
    """
    Connection state manager with SQLite
    """
    
    # State constants
    STATE_ONLINE = 'online'
    STATE_OFFLINE = 'offline'
    STATE_AWAY = 'away'
    
    def __init__(self, db_path='websocket.db'):
        """
        Initialize connection state
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        logger.info("Connection State initialized")
    
    def set_state(self, user_id, state):
        """
        Set user connection state
        
        Args:
            user_id: User ID
            state: Connection state (online, offline, away)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        last_seen = time.time()
        
        cursor.execute('''
            INSERT OR REPLACE INTO connection_state (user_id, state, last_seen, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        ''', (user_id, state, last_seen))
        
        conn.commit()
        conn.close()
        
        logger.info(f"State set for user {user_id}: {state}")
    
    def get_state(self, user_id):
        """
        Get user connection state
        
        Args:
            user_id: User ID
            
        Returns:
            State string or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT state, last_seen FROM connection_state WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                'state': row['state'],
                'last_seen': row['last_seen']
            }
        
        return None
    
    def get_online_users(self):
        """
        Get all online users
        
        Returns:
            List of user IDs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id FROM connection_state WHERE state = ?', (self.STATE_ONLINE,))
        rows = cursor.fetchall()
        
        conn.close()
        
        return [row[0] for row in rows]
    
    def get_all_states(self):
        """
        Get all user states
        
        Returns:
            Dictionary of user states
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id, state, last_seen FROM connection_state')
        rows = cursor.fetchall()
        
        conn.close()
        
        states = {}
        for row in rows:
            states[row['user_id']] = {
                'state': row['state'],
                'last_seen': row['last_seen']
            }
        
        return states
