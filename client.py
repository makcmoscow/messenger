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

class User:
    def __init__(self):
        pass

    def send_auth(self, conn):
        auth = self.messages.f_auth()
        conn.sendall(self.make_sendable(auth))

    @log
    def connect(self, IP, PORT):
        conn = socket.create_connection((IP, int(PORT)), 10)
        logger.info('connected')
        return conn

    @log
    def make_sendable(self, mess):
        jmessage = json.dumps(mess) + '\n\n'
        bjmessage = jmessage.encode()
        return bjmessage

    @log
    def send_message(self, conn, name_to=None, mess=None):
        message = self.messages.f_msg(name_to, mess)
        conn.sendall(self.make_sendable(message))
        return True

    @log
    def send_presence(self, conn):
        mess = self.messages.f_presence()
        conn.sendall(self.make_sendable(mess))
        # mess = create_presence(user_name)

    @log
    def get_message(self, conn):
        bjmess = conn.recv(1024)
        jmess = bjmess.decode()
        try:
            mess = json.loads(jmess)
        except Exception as e:
            print('error while json in get_message', e)
        else:
            return mess

    @log
    def chk_responce(self, resp):
        try:
            if resp['responce'] == 200:
                chk_result = True
            else:
                chk_result = False
            return chk_result
        except Exception as e:
            print('error', e)

    @log
    def send_online(self, conn):
        self.send_presence(conn)
        resp = self.get_message(conn)
        a = self.chk_responce(resp)
        return a

    def start(self):
        user = User()
        self.login = str(input('Enter your login '))
        self.password = str(input('Enter your password '))
        self.messages = Message(self.login, self.password)
        conn = self.connect(IP, PORT)
        if self.send_online(conn):
            if self.send_auth(conn) and self.recv_auth():
                wr1 = WriteThread(user)
                wr1.start()
                r1 = ReadThread(user)
                r1.start()
            else:
                self.start()
        else:
            print('server has problem. It\'s online, but don\'t responded')




class WriteThread(Thread):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def run(self):
        while True:
            name_to = str(input('Кому? '))
            mess = str(input('Введите ваше сообщение: '))
            try:
                a = self.user.send_message(self.user.conn, name_to, mess)
            except OSError:
                sys.exit(1)
            else:
                if a:
                    print('Message sended', '\n')



class ReadThread(Thread):
    def __init__(self, user):
        self.user = user
        super().__init__()
    def run(self):
        while True:
            try:
                mess = self.user.get_message(self.user.conn)
                if mess and 'message' in mess:
                    print()
                    print('message from ', mess['from'], '>>:  ', mess['message'])
            except OSError as e:
                pass




if __name__ == '__main__':
    user = User()
    user.start()





# send_presence(conn)
# send_auth(conn)



# while 1:
#     try:
#         mess = get_message(conn)
#         print(mess)
#     except OSError:
#         pass