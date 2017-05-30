#!/usr/bin/env python
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
import cgi
import redis

async_mode = None

app = Flask(__name__)
db = redis.StrictRedis('localhost', 6379, 0)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/room/<room_name>')
def roomhtml(room_name):
    return render_template('room.html', room=room_name)

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    db.hset('room.hash',message['room'],request.sid)
    allRooms()
    emit('room_rpy',{'type':'status','status':'join', 'msg': message['user']+' connected'},room=message['room'])


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    emit('room_rpy',{'type':'status', 'status':'left', 'msg': message['user']+' disconnected'},room=message['room'])
    emit('msg',{'type':'status', 'status':'left', 'room': message['room']},room=request.sid)


@socketio.on('close_room', namespace='/test')
def close(message):
    print(message['room'])
    emit('room_rpy', {'type': 'status','status':'close'},room=message['room'])
    close_room(message['room'])
    db.hdel('room.hash',message['room'])
    allRooms()

@socketio.on('room_msg', namespace='/test')
def send_room_message(message):
    emit('room_rpy',{'type':'reply','reply': message['msg'], 'user': message['user']},room=message['room'])

@socketio.on('nick_name', namespace='/test')
def nick_name(message):
    #db.set(request.sid,message['name'])
    if(db.hexists('user.hash',message['name'])):
        emit('msg',{'type':'connection', 'response': 0, 'msg': 'Key already exist. Try another key' })
    else:
        db.hset('user.hash', message['name'], request.sid)
        db.hset('session.hash', request.sid, message['name'])
        emit('msg',{'type':'connection', 'response': 1 })
        allRooms()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    name=db.hget('session.hash', request.sid)
    db.hdel('user.hash', name)
    db.hdel('session.hash', request.sid)
    allRooms()
    print('Client disconnected', request.sid)

def allRooms():
    emit('rooms', {'rooms': db.hkeys('room.hash')}, broadcast=True)
    emit('users', {'users': db.hkeys('user.hash')}, broadcast=True)

@socketio.on('private_msg', namespace='/test')
def send_private_message(message):
    if(db.hexists('user.hash',message['to'])):
        emit('private_rpy',{'type':'reply','reply': message['msg'], 'from': db.hget('session.hash', request.sid)},room=db.hget('user.hash', message['to']))
    else:
        allRooms()

if __name__ == '__main__':
    db.flushall()
    socketio.run(app, debug=True)
