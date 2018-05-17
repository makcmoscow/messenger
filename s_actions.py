from time import ctime
import alchemy
import time
import json
import mongo_DB
import copy

def presence(message, client):
    mess_login = message['user']['account_name']
    if mess_login == client.login:
        responce = create_responce(message, client.login, '200')#todo необходимо настроить rлиента на обработку ответов от сервера, потом написать аутентификацию
        send_message(responce, client.socket)

def authentication(message, client):
    mess_login = message['user']['account_name']
    mess_password = message['user']['password']
    if client.login != mess_login:
        pass
    else:





def msg(message, client):
    if client.login == message['to']:
        send_message(message, client.socket)
        return True
    return False


def create_responce(message, login, code):
    responce = {'responce': code,
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


def handler_unsended_mess(message, client):
    if message:
        action = message['action']
        actions[action](message, client)
        mongo_DB.update_sended(message)

actions = {'presence': presence, 'msg': msg, 'authentication': authentication}
