import socket
import select
import json
import time
from threading import Thread

# IP = '127.0.0.1'
# IP = input('Введите IP: ')

def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return (s.getsockname()[0])
IP = get_IP()
print('IP адрес сервера: ', IP)
PORT = 7777
serv_sock = socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM, proto=0)
serv_sock.setblocking(0)
serv_sock.bind((IP, PORT))
serv_sock.listen(5)
serv_sock.settimeout(0.2)
all_clients = []
messages = []
named_sockets = {}
writers = []
readers = []

class ChkClients(Thread):
    def __init__(self):
        super().__init__()
        self.readers = []
        self.writers = []
    def run(self):
        while True:
            try:
                conn, addr = serv_sock.accept()
            except OSError:
                pass
            else:
                all_clients.append(conn)
            finally:
                try:
                    self.writers, self.readers, self.errors = select.select(all_clients, all_clients, [])
                except:
                    pass
class ReadMessages(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global messages
        global named_sockets
        while True:
            for writer in chk.writers:
                try:
                    mess = get_message(writer)
                except Exception as e:
                    print('get_message error', e)
                else:
                    if mess is not None:
                        name_from, name_to = get_names(mess)
                        if name_from:
                            named_sockets[writer] = name_from
                            # print(named_sockets)
                            message = Message(writer, name_from, name_to, mess)
                            messages.append(message)

class WriteMessages(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global messages
        while True:
            for reader in chk.readers:
                name_to = get_name_socket(reader)
                for message in messages:
                    if message.name_to is None and message.name_from == reader:
                        # Probably it is presence
                        responce = {'responce': 200,
                                    'time': time.time()
                                    }
                        # print('responce sended')

                        if send_message(responce, reader):
                            messages.remove(message)
                        # readers.remove(reader)


                    elif message.name_to is not None and message.name_to == name_to:
                        # print(message.name_to)

                        if send_message(message.message, reader):  # Тут должна быть функция, подготавливающая сообщение перед отправкой
                            messages.remove(message)





def get_name_socket(socket):
    if socket in named_sockets: return named_sockets[socket]


def lookup(mess):
    if 'user' in mess:
        return mess['user'].get('account_name')
    return mess.get('from')

def get_names(mess):
    name_from = None
    name_to = None
    print('mess', mess)
    name_from = lookup(mess)
    name_to = mess.get('to')
    print(name_from, name_to)
    return name_from, name_to


def get_message(sock):
    jbmess = b''
    mess = None
    while not jbmess.endswith(b"\n\n"):
        try:
            jbmess += sock.recv(1024)
        except socket.error:
            pass
        else:
            jmess = jbmess.decode()
            mess = json.loads(jmess)
        finally:
            if mess is None:
                return None
            else:
                return mess


def send_message(message, sock):
    data = json.dumps(message).encode()
    sock.sendall(data)
    return True






# def send_message(message, messages, reader):
#     if message.name_to

class Message:
    def __init__(self, sock, name_from, name_to, message):
        self.sock = sock
        self.name_from = name_from
        self.name_to = name_to
        self.message = message

r_thr = ReadMessages()
w_thr = WriteMessages()
chk = ChkClients()
chk.start()
r_thr.start()
w_thr.start()




