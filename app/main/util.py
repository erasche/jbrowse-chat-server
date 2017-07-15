from flask_socketio import emit
from flask import session

def assertLogin():
    if 'account' not in session:
        emit('status', {
            'err': "Unauthenticated"
        })
        return False
    return True


def getRoom(message):
    if 'room' in message:
        return message['room']
    else:
        return 'unknown'


def processMessage(orig, message=None):
    data = {
        'user': session['account'],
    }
    if message:
        data['msg'] = message
    elif 'msg' in orig:
        data['msg'] = orig['msg']
    else:
        data['msg'] = ''

    data['msg'] = data['msg'].replace('/me', session['account']['name'])

    if 'loc' in orig:
        data['loc'] = orig['loc']

    if 'tracks' in orig:
        data['tracks'] = orig['tracks']

    return data

