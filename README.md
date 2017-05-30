# Chat-API-Python-SocketIO
One to One and Chat Room API Using SocketIO in Python

## Problem Statement
Write a chat API that should be able to provide capabilities to chat between individuals or groups. 
Create a user interface that would use the API to allow users to communicate with others via one on one or group mode in real-time.

## Steps to setup working environment
1. Install Redis Server
    - Ubuntu Command ```sudo apt-get install redis-server```
    - Redis ```port 6379```
2. Install Flask
    - ```pip install Flask```
3. Install Flask SocketIO
    - ```pip install flask-socketio```
    
## Endpoints

Register using Nick Name (Unique)
```
socket.emit('nick_name', {name: <UNIQUE-NAME> });
```

### One to One (Private Chat)

Get list of all Online Users
```
socket.on('users', function(msg) {
  //msg.users (List of users)
});
```

Send message to perticular user
```
socket.emit('private_msg', {msg: <MESSAGE-TO-SEND> , to: <RECIPIENT-UNIQUE-NAME> });
```

Get Private Message
```
socket.on('private_rpy', function(msg) {
    //msg.from (Nick name of Sender)
    //msg.reply (Message)
});
```

### Room

Create new room OR Join existing room
```
socket.emit('join', {room: <ROOM-NAME> , user: <UNIQUE-NAME> });
```

Send message to room
```
socket.emit('room_msg', {user: <UNIQUE-NAME> , room: <ROOM-NAME> , msg: <MESSAGE-TO-SEND> });
```

Leave the room
```
socket.emit('leave', {user: <UNIQUE-NAME> , room: <ROOM-NAME> });
```

Close the room
```
socket.emit('close_room', {room: <ROOM-NAME> });
```

Get list of all the Rooms
```
socket.on('rooms', function(msg) {
  //msg.rooms (List of rooms)
});
```
