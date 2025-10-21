"""
WebSocket Communication Hub - Main Demonstration
Shows examples of all WebSocket features
"""

import os
import time
from storage.database import init_database
from storage.message_store import MessageStore
from websocket.connection_manager import ConnectionManager
from websocket.connection_pool import ConnectionPool
from websocket.connection_state import ConnectionState
from rooms.room_manager import RoomManager
from messaging.offline_queue import OfflineQueue
from messaging.message_handler import MessageHandler


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_connection_management():
    """Demonstrate connection management"""
    print_section("1. WebSocket Connection Management")
    
    manager = ConnectionManager()
    
    # Add connections
    print("\n[EMOJI] Adding WebSocket connections:")
    manager.add_connection('conn-1', user_id=1, sid='sid-1')
    manager.add_connection('conn-2', user_id=1, sid='sid-2')
    manager.add_connection('conn-3', user_id=2, sid='sid-3')
    
    print(f"   [EMOJI] 3 connections added")
    
    # Get stats
    stats = manager.get_stats()
    print(f"\n[EMOJI] Connection Stats:")
    print(f"   Total connections: {stats['total_connections']}")
    print(f"   Online users: {stats['online_users']}")
    
    # Check if user is online
    is_online = manager.is_user_online(1)
    print(f"\n[EMOJI] User 1 online: {is_online}")


def demo_connection_pool():
    """Demonstrate connection pooling"""
    print_section("2. Connection Pooling")
    
    pool = ConnectionPool(max_connections_per_user=3)
    
    # Add connections
    print("\n[EMOJI] Testing connection limits:")
    for i in range(4):
        success = pool.add_connection(user_id=1, connection_id=f'conn-{i}')
        if success:
            print(f"   [EMOJI] Connection {i+1} added")
        else:
            print(f"   [EMOJI] Connection {i+1} rejected (limit reached)")
    
    # Get stats
    stats = pool.get_stats()
    print(f"\n[EMOJI] Pool Stats:")
    print(f"   Total connections: {stats['total_connections']}")
    print(f"   Max per user: {stats['max_per_user']}")


def demo_room_management():
    """Demonstrate room management"""
    print_section("3. Room-Based Communication")
    
    # Clean up old database
    db_path = 'demo.db'
    if os.path.exists(db_path):
        os.remove(db_path)
    
    init_database(db_path)
    manager = RoomManager(db_path)
    
    # Create room
    print("\n[EMOJI] Creating chat room:")
    manager.create_room('general', 'General Chat', created_by=1)
    print("   [EMOJI] Room 'general' created")
    
    # Join room
    print("\n[EMOJI] Users joining room:")
    manager.join_room('general', user_id=1)
    manager.join_room('general', user_id=2)
    manager.join_room('general', user_id=3)
    print("   [EMOJI] 3 users joined")
    
    # Get room members
    members = manager.get_room_members('general')
    print(f"\n[EMOJI] Room members: {members}")
    
    # Get room info
    info = manager.get_room_info('general')
    print(f"\n[EMOJI] Room Info:")
    print(f"   Name: {info['room_name']}")
    print(f"   Members: {info['member_count']}/{info['max_members']}")


def demo_offline_queue():
    """Demonstrate offline message queue"""
    print_section("4. Offline Message Queue")
    
    db_path = 'demo.db'
    queue = OfflineQueue(db_path, max_messages=10)
    
    # Queue messages for offline user
    print("\n[EMOJI] Queuing messages for offline user:")
    queue.add_message(user_id=99, message={'text': 'Message 1'}, sender_id=1)
    queue.add_message(user_id=99, message={'text': 'Message 2'}, sender_id=2)
    queue.add_message(user_id=99, message={'text': 'Message 3'}, sender_id=3)
    
    print("   [EMOJI] 3 messages queued")
    
    # Get queue size
    size = queue.get_queue_size(user_id=99)
    print(f"\n[EMOJI] Queue size for user 99: {size}")
    
    # Get queued messages
    messages = queue.get_messages(user_id=99)
    print(f"\n[EMOJI] Queued messages:")
    for msg in messages:
        print(f"   - From user {msg['sender_id']}: {msg['content']['text']}")


def demo_connection_state():
    """Demonstrate connection state"""
    print_section("5. Connection State Management")
    
    db_path = 'demo.db'
    state = ConnectionState(db_path)
    
    # Set states
    print("\n[EMOJI] Setting user states:")
    state.set_state(user_id=1, state=ConnectionState.STATE_ONLINE)
    state.set_state(user_id=2, state=ConnectionState.STATE_AWAY)
    state.set_state(user_id=3, state=ConnectionState.STATE_OFFLINE)
    
    print("   [EMOJI] States set for 3 users")
    
    # Get online users
    online_users = state.get_online_users()
    print(f"\n[EMOJI] Online users: {online_users}")
    
    # Get all states
    all_states = state.get_all_states()
    print(f"\n[EMOJI] All user states:")
    for user_id, user_state in all_states.items():
        print(f"   User {user_id}: {user_state['state']}")


def demo_message_handler():
    """Demonstrate message handling"""
    print_section("6. Message Processing")
    
    handler = MessageHandler()
    
    # Process message
    print("\n[EMOJI] Processing message:")
    raw_message = {
        'content': 'Hello, World!',
        'type': 'text',
        'recipient_id': 2
    }
    
    processed = handler.process_message(raw_message, sender_id=1)
    
    print(f"   [EMOJI] Message processed:")
    print(f"      ID: {processed['id']}")
    print(f"      From: {processed['sender_id']}")
    print(f"      To: {processed['recipient_id']}")
    print(f"      Content: {processed['content']}")
    
    # Validate message
    is_valid = handler.validate_message(raw_message)
    print(f"\n[EMOJI] Message valid: {is_valid}")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print("  WebSocket Communication Hub - Demonstration")
    print("=" * 70)
    
    try:
        demo_connection_management()
        demo_connection_pool()
        demo_room_management()
        demo_offline_queue()
        demo_connection_state()
        demo_message_handler()
        
        print("\n" + "=" * 70)
        print("  All Demonstrations Completed!")
        print("=" * 70)
        print("\nKey Features Demonstrated:")
        print("  1. Connection Management - Track WebSocket connections")
        print("  2. Connection Pooling - Limit connections per user")
        print("  3. Room Management - Group-based messaging")
        print("  4. Offline Queue - Store messages for offline users")
        print("  5. Connection State - Track online/offline status")
        print("  6. Message Handler - Process and validate messages")
        print("\nTo run WebSocket server:")
        print("  python api/app.py")
        print("\nTo run tests:")
        print("  python tests.py")
        print()
        
        # Cleanup
        if os.path.exists('demo.db'):
            os.remove('demo.db')
        
    except Exception as e:
        print(f"\n[EMOJI] Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
