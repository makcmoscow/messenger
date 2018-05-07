# from Const import IP, PORT, TIMEOUT
# IP = '127.0.0.1'
PORT = 7777
IP = input('Введите IP: ')
TIMEOUT = 10
import socket
import time
import json
from type_msg import *
from threading import Thread
import sys
import client_logger
import logging
from decorators import Log
logger = logging.getLogger('client')
log = Log(logger)


user_name = input('Введите имя пользователя: ')
messages = Message(user_name)
class WriteThread(Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            name_to = input('Кому? ')
            mess = input('Введите ваше сообщение: ')
            try:
                a = send_message(conn, name_to, mess)
            except OSError:
                sys.exit(1)
            else:
                if a:
                    print('Message sended', '\n')



class ReadThread(Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            try:
                mess = get_message(conn)
                if 'message' in mess:
                    print()
                    print('message from ', mess['from'], '>>:  ', mess['message'])
            except OSError as e:
                pass



@log
def connect(IP, PORT):
    conn = socket.create_connection((IP, int(PORT)), 10)
    logger.info('123')
    return conn

@log
def make_sendable(mess):
    jmessage = json.dumps(mess)+'\n\n'
    bjmessage = jmessage.encode()
    return bjmessage

@log
def send_message(conn, name_to=None, mess=None):
    message = messages.f_msg(name_to, mess)
    conn.sendall(make_sendable(message))
    return True

@log
def send_presence(conn):
    mess = messages.f_presence()
    conn.sendall(make_sendable(mess))
    # mess = create_presence(user_name)

@log
def get_message(conn):
    bjmess = conn.recv(1024)
    jmess = bjmess.decode()
    try:
        mess = json.loads(jmess)
    except Exception as e:
        pass
    else:
        return mess

@log
def chk_responce(resp):
    try:
        if resp['responce'] == 200:
            conn_well = True
        else:
            conn_well = False
        return conn_well
    except Exception as e:
        print('error', e)

@log
def send_online(conn):
    send_presence(conn)
    resp = get_message(conn)
    a = chk_responce(resp)
    return a

conn = connect(IP, PORT)
send_presence(conn)

wr1 = WriteThread()
wr1.start()
r1 = ReadThread()
r1.start()

# while 1:
#     try:
#         mess = get_message(conn)
#         print(mess)
#     except OSError:
#         pass