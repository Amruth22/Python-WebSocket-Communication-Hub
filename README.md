# WebSocket Communication Hub

Educational Python application demonstrating **WebSocket connection management**, **real-time communication hub**, **connection pooling**, **message broadcasting**, **room-based communication**, **connection state management**, and **message queuing for offline users** with **SQLite3 storage**.

## Features

### 🔌 WebSocket Connection Management
- **Connection Tracking** - Track all active WebSocket connections
- **Connection Lifecycle** - Connect, disconnect, reconnect handling
- **Connection Validation** - Verify connection health
- **Activity Tracking** - Update last activity timestamps
- **Multi-Connection Support** - Multiple connections per user

### 🌐 Real-Time Communication Hub
- **Central Message Hub** - Route messages between clients
- **Direct Messaging** - Send to specific users
- **Message Routing** - Route based on message type
- **Instant Delivery** - Real-time message delivery
- **Offline Handling** - Queue for offline users

### 🏊 Connection Pooling
- **Connection Limits** - Max connections per user
- **Pool Management** - Add/remove connections
- **Pool Statistics** - Track pool usage
- **Connection Validation** - Verify before adding

### 📢 Message Broadcasting
- **Broadcast to All** - Send to all connected clients
- **Broadcast to Room** - Send to room members
- **Broadcast to Users** - Send to specific users
- **Selective Broadcasting** - Exclude specific users

### 🏠 Room-Based Communication
- **Room Creation** - Create chat rooms
- **Join/Leave Rooms** - User room management
- **Room Messages** - Send to room members
- **Room Persistence** - Store rooms in SQLite
- **Member Management** - Track room members

### 📊 Connection State Management
- **Online/Offline Status** - Track user presence
- **State Persistence** - Store state in SQLite
- **Last Seen Tracking** - Track last activity
- **Presence System** - Show who's online
- **State Updates** - Real-time state changes

### 📬 Offline Message Queue
- **Message Queuing** - Store messages for offline users
- **SQLite Persistence** - Messages survive restarts
- **Automatic Delivery** - Deliver when user comes online
- **Queue Management** - Size limits, cleanup
- **Message Tracking** - Delivered/undelivered status

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Amruth22/Python-WebSocket-Communication-Hub.git
cd Python-WebSocket-Communication-Hub
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Demonstrations
```bash
python main.py
```

### 5. Run WebSocket Server
```bash
python api/app.py
```

The server will be available at `http://localhost:5000`

### 6. Run Tests
```bash
python tests.py
```

## Project Structure

```
Python-WebSocket-Communication-Hub/
│
├── websocket/
│   ├── connection_manager.py    # Connection management
│   ├── connection_pool.py       # Connection pooling
│   └── connection_state.py      # State tracking (SQLite)
│
├── hub/
│   ├── communication_hub.py     # Central hub
│   ├── message_router.py        # Message routing
│   └── broadcast_manager.py     # Broadcasting
│
├── rooms/
│   ├── room_manager.py          # Room management (SQLite)
│   └── room_store.py            # Room storage
│
├── messaging/
│   ├── message_queue.py         # In-memory queue
│   ├── offline_queue.py         # Offline queue (SQLite)
│   └── message_handler.py       # Message processing
│
├── storage/
│   ├── database.py              # SQLite setup
│   └── message_store.py         # Message persistence
│
├── api/
│   └── app.py                   # Flask-SocketIO server
│
├── main.py                      # Demonstration
├── tests.py                     # 10 unit tests
└── README.md                    # This file
```

## Database Schema

### Rooms Table
```sql
CREATE TABLE rooms (
    room_id TEXT PRIMARY KEY,
    room_name TEXT NOT NULL,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_private BOOLEAN DEFAULT 0,
    max_members INTEGER DEFAULT 100
)
```

### Room Members Table
```sql
CREATE TABLE room_members (
    room_id TEXT,
    user_id INTEGER,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (room_id, user_id)
)
```

### Messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    recipient_id INTEGER,
    room_id TEXT,
    message_type TEXT,
    content TEXT,
    delivered BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Connection State Table
```sql
CREATE TABLE connection_state (
    user_id INTEGER PRIMARY KEY,
    state TEXT,
    last_seen REAL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Usage Examples

### WebSocket Client (JavaScript)

```javascript
// Connect to WebSocket server
const socket = io('http://localhost:5000');

// Register user
socket.emit('register', { user_id: 1 });

// Listen for registration confirmation
socket.on('registered', (data) => {
    console.log('Registered:', data);
});

// Send direct message
socket.emit('message', {
    sender_id: 1,
    recipient_id: 2,
    content: 'Hello!',
    type: 'text'
});

// Join room
socket.emit('join_room', {
    room_id: 'general',
    user_id: 1
});

// Send room message
socket.emit('room_message', {
    room_id: 'general',
    sender_id: 1,
    content: 'Hello room!'
});

// Listen for messages
socket.on('message', (data) => {
    console.log('Message received:', data);
});

// Listen for room messages
socket.on('room_message', (data) => {
    console.log('Room message:', data);
});

// Broadcast to all
socket.emit('broadcast', {
    sender_id: 1,
    content: 'Announcement to all!'
});
```

### Python Client

```python
import socketio

# Create client
sio = socketio.Client()

# Connect
sio.connect('http://localhost:5000')

# Register
sio.emit('register', {'user_id': 1})

# Send message
sio.emit('message', {
    'sender_id': 1,
    'recipient_id': 2,
    'content': 'Hello from Python!'
})

# Listen for messages
@sio.on('message')
def on_message(data):
    print(f"Message received: {data}")

# Disconnect
sio.disconnect()
```

## WebSocket Events

### Client → Server

- **register** - Register user connection
- **message** - Send direct message
- **join_room** - Join a room
- **leave_room** - Leave a room
- **room_message** - Send message to room
- **broadcast** - Broadcast to all users

### Server → Client

- **connected** - Connection established
- **registered** - Registration successful
- **message** - Direct message received
- **room_message** - Room message received
- **broadcast** - Broadcast message
- **user_joined** - User joined room
- **user_left** - User left room
- **error** - Error occurred

## Testing

Run the comprehensive test suite:

```bash
python tests.py
```

### Test Coverage (10 Tests)

1. ✅ **Connection Management** - Test add/remove connections
2. ✅ **Connection Pool** - Test connection limits
3. ✅ **Room Creation** - Test room management
4. ✅ **Room Messaging** - Test room-based messages
5. ✅ **Connection State** - Test online/offline status
6. ✅ **Offline Queue** - Test message queuing
7. ✅ **Message Delivery** - Test delivery tracking
8. ✅ **Message Store** - Test SQLite persistence
9. ✅ **Message Handler** - Test message processing
10. ✅ **Room Persistence** - Test room storage

## Educational Notes

### 1. WebSocket vs HTTP

**HTTP:**
- Request/response model
- Client initiates
- One-way communication

**WebSocket:**
- Full-duplex communication
- Bi-directional
- Real-time updates
- Persistent connection

### 2. Why Connection Pooling?

**Benefits:**
- Limit resource usage
- Prevent abuse
- Fair resource allocation
- Better performance

### 3. Offline Message Queue

**Purpose:**
- Don't lose messages
- Deliver when user returns
- Better user experience
- Message persistence

### 4. Room-Based Communication

**Use Cases:**
- Group chat
- Team collaboration
- Game lobbies
- Live events

## Production Considerations

For production use:

1. **Scalability:**
   - Use Redis for pub/sub
   - Implement sticky sessions
   - Add load balancing
   - Use message broker

2. **Persistence:**
   - Use PostgreSQL/MySQL
   - Implement message archiving
   - Add backup strategies

3. **Security:**
   - Implement authentication
   - Add message encryption
   - Validate all input
   - Rate limiting

4. **Monitoring:**
   - Track connection count
   - Monitor message throughput
   - Alert on errors
   - Performance metrics

## Dependencies

- **Flask 3.0.0** - Web framework
- **Flask-SocketIO 5.3.5** - WebSocket support
- **python-socketio 5.10.0** - SocketIO implementation
- **python-dotenv 1.0.0** - Environment variables
- **pytest 7.4.3** - Testing framework
- **sqlite3** - Database (built-in)

## License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Happy Coding! 🚀**
