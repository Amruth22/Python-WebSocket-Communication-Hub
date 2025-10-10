# MCQ Questions - WebSocket Communication Hub

## Instructions
Choose the best answer for each question. Each question has only one correct answer.

---

### Question 1: WebSocket Protocol
What is the main advantage of WebSocket over HTTP for real-time communication?

A) WebSocket is faster for all types of requests  
B) WebSocket provides full-duplex bidirectional communication over a single persistent connection  
C) WebSocket uses less bandwidth for static content  
D) WebSocket is easier to implement  

**Answer: B**

---

### Question 2: Connection Pooling
Why implement connection pooling for WebSocket connections?

A) To make connections faster  
B) To limit the number of connections per user and prevent resource exhaustion  
C) To encrypt connections  
D) To compress data  

**Answer: B**

---

### Question 3: Message Broadcasting
What does broadcasting a message mean in WebSocket communication?

A) Sending a message to the database  
B) Sending a message to multiple clients simultaneously  
C) Encrypting a message  
D) Deleting a message  

**Answer: B**

---

### Question 4: Room-Based Communication
What is a room in WebSocket communication?

A) A physical server room  
B) A logical group where members can send and receive messages within that group  
C) A database table  
D) A type of message  

**Answer: B**

---

### Question 5: Offline Message Queue
Why queue messages for offline users?

A) To delete messages  
B) To ensure messages are delivered when the user reconnects, preventing message loss  
C) To slow down the system  
D) To encrypt messages  

**Answer: B**

---

### Question 6: Connection State
What does tracking connection state (online/offline/away) enable?

A) Faster message delivery  
B) Presence awareness so users know who is available for real-time communication  
C) Data encryption  
D) Message compression  

**Answer: B**

---

### Question 7: Full-Duplex Communication
What does full-duplex communication mean?

A) Communication in one direction only  
B) Both client and server can send and receive data simultaneously  
C) Communication that requires two connections  
D) Encrypted communication  

**Answer: B**

---

### Question 8: WebSocket Handshake
How does a WebSocket connection start?

A) Directly as a WebSocket connection  
B) As an HTTP request that upgrades to WebSocket protocol  
C) Through FTP  
D) Through email  

**Answer: B**

---

### Question 9: Message Persistence
Why persist messages in SQLite for offline users?

A) To make the application slower  
B) To ensure messages survive server restarts and are delivered when users reconnect  
C) To increase database size  
D) Persistence is not necessary  

**Answer: B**

---

### Question 10: Connection Limit
What happens when a user reaches their connection limit?

A) All connections are closed  
B) New connection attempts are rejected to prevent resource exhaustion  
C) The server crashes  
D) Old connections are automatically deleted  

**Answer: B**

---

### Question 11: Room Membership
How is room membership typically managed?

A) In browser cookies  
B) In a database table linking users to rooms they've joined  
C) In text files  
D) Room membership is not tracked  

**Answer: B**

---

### Question 12: Heartbeat/Ping-Pong
What is the purpose of WebSocket ping-pong (heartbeat)?

A) To play games  
B) To keep the connection alive and detect disconnected clients  
C) To send messages faster  
D) To encrypt data  

**Answer: B**

---

### Question 13: Message Routing
In a communication hub, what does message routing do?

A) Deletes messages  
B) Directs messages to the appropriate destination (user, room, or broadcast)  
C) Encrypts messages  
D) Compresses messages  

**Answer: B**

---

### Question 14: Presence System
What is a presence system in real-time communication?

A) A security system  
B) A system that shows which users are online, offline, or away  
C) A message encryption system  
D) A backup system  

**Answer: B**

---

### Question 15: WebSocket vs Long Polling
What is the main advantage of WebSocket over long polling?

A) WebSocket is older technology  
B) WebSocket maintains a persistent connection, reducing overhead compared to repeated HTTP requests  
C) WebSocket uses more bandwidth  
D) WebSocket is only for chat applications  

**Answer: B**

---

## Answer Key Summary

1. B - Full-duplex bidirectional communication  
2. B - Limit connections, prevent exhaustion  
3. B - Send to multiple clients simultaneously  
4. B - Logical group for group messaging  
5. B - Deliver when user reconnects  
6. B - Presence awareness for users  
7. B - Simultaneous send/receive  
8. B - HTTP upgrade to WebSocket  
9. B - Survive restarts, ensure delivery  
10. B - Reject new connections  
11. B - Database table linking users to rooms  
12. B - Keep alive, detect disconnects  
13. B - Direct to appropriate destination  
14. B - Show online/offline/away status  
15. B - Persistent connection, less overhead  

---

**Total Questions: 15**  
**Topics Covered:** WebSocket protocol, Connection management, Message broadcasting, Room-based communication, Offline queuing, Connection state, Presence system, Message routing, Full-duplex communication, Heartbeat mechanism

**Difficulty Level:** Beginner to Intermediate  
**Passing Score:** 80% (12/15 correct answers)
