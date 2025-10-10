"""
Database Setup
SQLite database initialization for WebSocket hub
"""

import sqlite3
import logging

logger = logging.getLogger(__name__)


def init_database(db_path='websocket.db'):
    """
    Initialize SQLite database with all required tables
    
    Args:
        db_path: Path to database file
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Rooms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            room_id TEXT PRIMARY KEY,
            room_name TEXT NOT NULL,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_private BOOLEAN DEFAULT 0,
            max_members INTEGER DEFAULT 100
        )
    ''')
    
    # Room members table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS room_members (
            room_id TEXT,
            user_id INTEGER,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (room_id, user_id),
            FOREIGN KEY (room_id) REFERENCES rooms(room_id)
        )
    ''')
    
    # Messages table (for persistence and offline queue)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            recipient_id INTEGER,
            room_id TEXT,
            message_type TEXT,
            content TEXT,
            delivered BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            delivered_at TIMESTAMP
        )
    ''')
    
    # Connection state table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS connection_state (
            user_id INTEGER PRIMARY KEY,
            state TEXT,
            last_seen REAL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_recipient ON messages(recipient_id, delivered)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_room ON messages(room_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_members_user ON room_members(user_id)')
    
    conn.commit()
    conn.close()
    
    logger.info(f"Database initialized: {db_path}")


def get_connection(db_path='websocket.db'):
    """
    Get database connection
    
    Args:
        db_path: Path to database file
        
    Returns:
        SQLite connection
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
