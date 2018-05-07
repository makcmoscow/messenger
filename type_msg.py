from time import ctime

class Message:
    def __init__(self, login):
        self.login = login

    def f_presence(self):
        presence = {
            'action': 'presence',
            'time': ctime(),
            'type': 'status',
            'user': {
                'account_name': self.login,
                'status': 'OK'
            }
        }
        return presence

    def f_auth(self):
        auth_message = {
            'action': 'authenticate',
            'time': ctime(),
            'user': {
                'account_name': self.login,
                'password': 'CorrectHorseBatteryStaple'
            }
        }
        return auth_message

    def f_msg(self, name_to, mess):
        msg = {
            'action': 'msg',
            'time': ctime(),
            'to': name_to,
            'from': self.login,
            'encoding': 'utf-8',
            'message': mess
        }
        return msg

    def f_join(self):
        join_chat = {
            'action': 'join',
            'time': ctime(),
            'room': '#room_name'
        }
        return join_chat

    def f_leave(self):
        leave_chat = {
            'action': 'leave',
            'time': ctime(),
            'room': '#room_name'
        }
        return leave_chat

# def f_presence(user_name):
#     presence = {
#         'action': 'presence',
#         'time': ctime(),
#         'type': 'status',
#         'user': {
#             'account_name': user_name,
#             'status': 'OK'
#         }
#     }
#     return presence

# def f_auth():
#     auth_message = {
#         'action': 'authenticate',
#         'time': ctime(),
#         'user': {
#             'account_name': 'CodeMaverick',
#             'password': 'CorrectHorseBatteryStaple'
#         }
#     }
#     return auth_message

# def f_msg(user_name, name_to, mess):
#     msg = {
#         'action': 'msg',
#         'time': ctime(),
#         'to': name_to,
#         'from': user_name,
#         'encoding': 'utf-8',
#         'message': mess
#     }
#     return msg

# def f_join():
#     join_chat = {
#         'action': 'join',
#         'time': ctime(),
#         'room': '#room_name'
#     }
#     return join_chat

# def f_leave():
#     leave_chat = {
#         'action': 'leave',
#         'time': ctime(),
#         'room': '#room_name'
#     }
#     return leave_chat

def f_quit():
    quit = {
        'action': 'quit'
    }
    return quit

def f_probe():
    probe = {
        'action': 'probe',
        'time': ctime()
    }
    return probe

def f_alert(number, text):
    alert = {
        'response': number,
        'time': ctime(),
        'alert': text
    }
    return alert

def f_error(number, text):
    error = {
        'response': number,
        'time': ctime(),
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
if __name__ == '__main__':
    a = '200'
    a = f_alert(a, code[a])
    print(a)