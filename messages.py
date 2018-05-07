import time


def f_presence(login):
    presence = {
        'action': 'presence',
        'time': time.time(),
        'type': 'status',
        'user': {
            'account_name': login,
            'status': 'OK'
        }
    }
    return presence

def f_auth(login):
    auth_message = {
        'action': 'authenticate',
        'time': time.time(),
        'user': {
            'account_name': login,
            'password': 'CorrectHorseBatteryStaple'
        }
    }
    return auth_message

def f_msg(login):
    msg = {
        'action': 'msg',
        'time': time.time(),
        'to': 'account_name',
        'from': login,
        'encoding': 'utf-8',
        'message': 'MESSAGE'
    }
    return msg

def f_join():
    join_chat = {
        'action': 'join',
        'time': time.time(),
        'room': '#room_name'
    }
    return join_chat

def f_leave():
    leave_chat = {
        'action': 'leave',
        'time': time.time(),
        'room': '#room_name'
    }
    return leave_chat

def f_quit():
    quit = {
        'action': 'quit'
    }
    return quit

def f_probe():
    probe = {
        'action': 'probe',
        'time': time.time()
    }
    return probe

def f_alert(number, text):
    alert = {
        'response': number,
        'time': time.time(),
        'alert': text
    }
    return alert

def f_error(number, text):
    error = {
        'response': number,
        'time': time.time(),
        'error': text
    }
    return error


code = {
    '100': 'based notification',
    '101': 'important notice',
    '200': 'OK',
    '201': 'created',
    '202': 'accepted',

    '400': 'incorrect json object',
    '401': 'not authorized',
    '402': 'incorrect login or password',
    '403': 'user forbidden',
    '404': 'user or chat not found in server',
    '409': 'conflict! login is already in use',
    '410': 'user offline',
    '500': 'server error'
}
