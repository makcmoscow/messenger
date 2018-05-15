from time import ctime
import alchemy
import time
import json
import mongo_DB
import copy

def presence(message, sock, named_sockets):
    login = named_sockets[sock]
    mess_login = message['user']['account_name']
    if mess_login == login:
        responce = create_responce(message, login)
        send_message(responce, sock)


    # mess_password = message['user']['password']
    # auth_is_ok = mongo_DB.autentification(login, password)
    # if auth_is_ok:
    # else:
    # print('login {} or password {} wrong'.format(login, password))
    # return auth_is_ok







def msg(message, sock, named_sockets):
    if named_sockets[sock] == message['to']:
        send_message(message, sock)
        return True
    return False




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
    # print('message', message)
    new_message = copy.copy(message)
    if '_id' in message:
        new_message.pop('_id')
    data = json.dumps(new_message).encode()
    sock.sendall(data)
    return True

def handler_unsended_mess(message, reader, named_sockets):
    if message:
        action = message['action']
        actions[action](message, reader, named_sockets)
        mongo_DB.update_sended(message)


