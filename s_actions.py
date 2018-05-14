from time import ctime
import alchemy
import time
import json
import mongo_DB

def presence(message, sock, named_sockets):
    login = message['user']['account_name']
    password = message['user']['password']
    # alchemy.chk_DB()
    # alchemy.chk_uexist_DB(login, password)
    responce = create_responce(message, login)
    if named_sockets[sock] == login:
        send_message(responce, sock)



def msg(message, sock, named_sockets):
    print('name in message', message['to'])
    print('named socked and name: ', named_sockets, named_sockets[sock])
    if named_sockets[sock] == message['to']:
        send_message(message['message'], sock)




actions = {'presence': presence, 'msg': msg}


def get_username_pass(message):
    login = message.message['user']['account_name']
    password = message.message['user']['password']
    return login, password

def create_responce(message, login):
    responce = {'responce': 200,
                'time': time.time(),
                'to': login
                }
    return responce

def send_message(message, sock):
    print('message', message)
    data = json.dumps(message).encode()
    sock.sendall(data)
    return True
# action = message['action']

# c = actions[action]()
# print(c)
# actions[action]

