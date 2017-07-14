from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from util import assertLogin, getRoom, processMessage


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    if not assertLogin():
        return
    room = getRoom(message)

    join_room(room)
    emit('status', processMessage({}, '/me has entered the room.'), room=room)

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    if not assertLogin():
        return
    room = getRoom(message)

    # Location messages are treated specially
    if message['msg'].startswith('[location '):
        emit('status', processMessage(message), room=room)
    else:
        emit('message', processMessage(message), room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    if not assertLogin():
        return
    room = getRoom(message)

    leave_room(room)
    emit('status', processMessage(message, '/me has left the room.'), room=room)
