"""
Comprehensive Unit Tests for WebSocket Communication Hub
Tests connections, rooms, messaging, state, and offline queue
"""

import unittest
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


class WebSocketCommunicationTestCase(unittest.TestCase):
    """Unit tests for WebSocket Communication Hub"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test configuration"""
        print("\n" + "=" * 60)
        print("WebSocket Communication Hub - Unit Test Suite")
        print("=" * 60)
        print("Testing: Connections, Rooms, Messages, State, Queue")
        print("=" * 60 + "\n")
        
        # Use test database
        cls.db_path = 'test_websocket.db'
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
        
        init_database(cls.db_path)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
    
    # Test 1: Connection Management
    def test_01_connection_management(self):
        """Test WebSocket connection management"""
        print("\n1. Testing connection management...")
        
        manager = ConnectionManager()
        
        # Add connection
        manager.add_connection('conn-1', user_id=1, sid='sid-1')
        
        self.assertIn('conn-1', manager.connections)
        print("   ✅ Connection added")
        
        # Get connection
        conn = manager.get_connection('conn-1')
        self.assertEqual(conn['user_id'], 1)
        print(f"   ✅ Connection retrieved for user {conn['user_id']}")
        
        # Remove connection
        manager.remove_connection('conn-1')
        self.assertNotIn('conn-1', manager.connections)
        print("   ✅ Connection removed")
    
    # Test 2: Connection Pool
    def test_02_connection_pool(self):
        """Test connection pooling"""
        print("\n2. Testing connection pool...")
        
        pool = ConnectionPool(max_connections_per_user=3)
        
        # Add connections
        pool.add_connection(user_id=1, connection_id='conn-1')
        pool.add_connection(user_id=1, connection_id='conn-2')
        pool.add_connection(user_id=1, connection_id='conn-3')
        
        count = pool.get_user_connection_count(user_id=1)
        self.assertEqual(count, 3)
        print(f"   ✅ 3 connections added")
        
        # Try to exceed limit
        success = pool.add_connection(user_id=1, connection_id='conn-4')
        self.assertFalse(success)
        print("   ✅ 4th connection rejected (limit reached)")
    
    # Test 3: Room Creation
    def test_03_room_creation(self):
        """Test room creation and management"""
        print("\n3. Testing room creation...")
        
        manager = RoomManager(self.db_path)
        
        # Create room
        manager.create_room('test-room', 'Test Room', created_by=1)
        
        # Get room info
        info = manager.get_room_info('test-room')
        
        self.assertIsNotNone(info)
        self.assertEqual(info['room_name'], 'Test Room')
        print(f"   ✅ Room created: {info['room_name']}")
    
    # Test 4: Room Messaging
    def test_04_room_messaging(self):
        """Test room-based messaging"""
        print("\n4. Testing room messaging...")
        
        manager = RoomManager(self.db_path)
        
        # Create room
        manager.create_room('chat-room', 'Chat Room', created_by=1)
        
        # Join room
        manager.join_room('chat-room', user_id=1)
        manager.join_room('chat-room', user_id=2)
        
        # Get members
        members = manager.get_room_members('chat-room')
        
        self.assertEqual(len(members), 2)
        print(f"   ✅ 2 users joined room")
        
        # Leave room
        manager.leave_room('chat-room', user_id=1)
        
        members = manager.get_room_members('chat-room')
        self.assertEqual(len(members), 1)
        print(f"   ✅ User left room, {len(members)} remaining")
    
    # Test 5: Connection State
    def test_05_connection_state(self):
        """Test connection state management"""
        print("\n5. Testing connection state...")
        
        state = ConnectionState(self.db_path)
        
        # Set state
        state.set_state(user_id=1, state=ConnectionState.STATE_ONLINE)
        state.set_state(user_id=2, state=ConnectionState.STATE_OFFLINE)
        
        print("   ✅ States set for 2 users")
        
        # Get state
        user1_state = state.get_state(user_id=1)
        self.assertEqual(user1_state['state'], ConnectionState.STATE_ONLINE)
        print(f"   ✅ User 1 state: {user1_state['state']}")
        
        # Get online users
        online = state.get_online_users()
        self.assertIn(1, online)
        print(f"   ✅ Online users: {online}")
    
    # Test 6: Offline Message Queue
    def test_06_offline_message_queue(self):
        """Test offline message queuing"""
        print("\n6. Testing offline message queue...")
        
        queue = OfflineQueue(self.db_path, max_messages=10)
        
        # Add messages
        queue.add_message(user_id=99, message={'text': 'Message 1'}, sender_id=1)
        queue.add_message(user_id=99, message={'text': 'Message 2'}, sender_id=2)
        
        print("   ✅ 2 messages queued")
        
        # Get queue size
        size = queue.get_queue_size(user_id=99)
        self.assertEqual(size, 2)
        print(f"   ✅ Queue size: {size}")
        
        # Get messages
        messages = queue.get_messages(user_id=99)
        self.assertEqual(len(messages), 2)
        print(f"   ✅ Retrieved {len(messages)} messages")
    
    # Test 7: Message Delivery
    def test_07_message_delivery(self):
        """Test message delivery and marking"""
        print("\n7. Testing message delivery...")
        
        queue = OfflineQueue(self.db_path)
        
        # Add message
        msg_id = queue.add_message(user_id=88, message={'text': 'Test'}, sender_id=1)
        
        # Get undelivered
        messages = queue.get_messages(user_id=88)
        self.assertEqual(len(messages), 1)
        print(f"   ✅ 1 undelivered message")
        
        # Mark delivered
        queue.mark_delivered(msg_id)
        
        # Should be empty now
        messages = queue.get_messages(user_id=88)
        self.assertEqual(len(messages), 0)
        print(f"   ✅ Message marked as delivered")
    
    # Test 8: Message Store
    def test_08_message_store(self):
        """Test message persistence"""
        print("\n8. Testing message store...")
        
        store = MessageStore(self.db_path)
        
        # Save message
        msg_id = store.save_message(
            sender_id=1,
            recipient_id=2,
            message_type='text',
            content={'text': 'Hello'}
        )
        
        self.assertIsNotNone(msg_id)
        print(f"   ✅ Message saved with ID: {msg_id}")
        
        # Get undelivered
        messages = store.get_undelivered_messages(user_id=2)
        self.assertGreaterEqual(len(messages), 1)
        print(f"   ✅ Undelivered messages: {len(messages)}")
    
    # Test 9: Message Handler
    def test_09_message_handler(self):
        """Test message processing"""
        print("\n9. Testing message handler...")
        
        handler = MessageHandler()
        
        # Process message
        raw_message = {
            'content': 'Test message',
            'type': 'text',
            'recipient_id': 2
        }
        
        processed = handler.process_message(raw_message, sender_id=1)
        
        self.assertIn('id', processed)
        self.assertIn('timestamp', processed)
        self.assertEqual(processed['sender_id'], 1)
        print(f"   ✅ Message processed with ID: {processed['id']}")
        
        # Validate message
        is_valid = handler.validate_message(raw_message)
        self.assertTrue(is_valid)
        print(f"   ✅ Message validation: {is_valid}")
    
    # Test 10: Room Persistence
    def test_10_room_persistence(self):
        """Test room data persistence"""
        print("\n10. Testing room persistence...")
        
        manager = RoomManager(self.db_path)
        
        # Create room
        manager.create_room('persist-room', 'Persistent Room', created_by=1)
        
        # Join room
        manager.join_room('persist-room', user_id=1)
        
        # Get user rooms
        user_rooms = manager.get_user_rooms(user_id=1)
        
        self.assertIn('persist-room', user_rooms)
        print(f"   ✅ User rooms: {user_rooms}")
        
        # List all rooms
        all_rooms = manager.list_rooms()
        self.assertGreater(len(all_rooms), 0)
        print(f"   ✅ Total rooms: {len(all_rooms)}")


def run_tests():
    """Run all unit tests"""
    # Create test suite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(WebSocketCommunicationTestCase)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")
    
    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    if not result.failures and not result.errors:
        print("\n🎉 ALL TESTS PASSED! 🎉")
    
    print("=" * 60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("WebSocket Communication Hub - Unit Test Suite")
    print("=" * 60)
    
    try:
        success = run_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
