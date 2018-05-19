from time import ctime
import time
import json
import mongo_DB
import copy

# re_actions =

def chk_password(client, mess_password):
    client_db = mongo_DB.found_user(client.login)
    if client_db['password'] == mess_password:
        return True
    return False


def presence(message, client):
    responce = create_responce(client.login, '200')#todo необходимо настроить rлиента на обработку ответов от сервера, потом написать аутентификацию
    send_message(responce, client.socket)

def authentication(message, client):
    mess_password = message['user']['password']
    if chk_password(client, mess_password):
        client.auth = True


def msg(message, client):
    if client.login == message['to']:
        send_message(message, client.socket)
        return True
    return False


def create_responce(login, code):
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


def chk_reciever(message, client):
    try:
        mess_login = message['user']['account_name']
    except KeyError:
        mess_login = message['to']
    finally:
        if mess_login == client.login:
            return True
        else:
            return False


def handler_unsended_mess(message, client):
    if message and chk_reciever(message, client):
        action = message['action']
        actions[action](message, client)
        mongo_DB.update_sended(message)
    else:
        pass

actions = {'presence': presence, 'msg': msg, 'authentication': authentication}
