import socket
import select
import json
import time
import s_actions
import mongo_DB
import asyncio



class Client:
    def __init__(self, socket):
        self.socket = socket
        self.login = None
        self.auth = None
        self.password = False

class Server:
    all_clients = []
    named_sockets = {}
    def __init__(self):
        self.PORT = 7777
        self.IP = self.get_IP()
        self.sock = self.create_serv_sock()

    def get_name_socket(self, socket):
        if socket in Server.named_sockets: return Server.named_sockets[socket]

    def get_IP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return (s.getsockname()[0])

    def create_serv_sock(self):
        serv_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0)
        serv_sock.setblocking(0)
        serv_sock.bind((self.IP, self.PORT))
        serv_sock.listen(5)
        serv_sock.settimeout(0.2)
        return serv_sock


async def ChkClients(serv):
    while True:
        try:
            conn, addr = serv.sock.accept()
            new_client = Client(conn)
        except OSError:
            await asyncio.sleep(0.1)
        else:
            Server.all_clients.append(new_client)
        # finally:
        #     if Server.all_clients:
        #         Server.writers, Server.readers, Server.errors = select.select(Server.all_clients, Server.all_clients, [])






async def ReadMessages():
    while True:
        # for writer in Server.writers:
        #     mess = get_message(writer)
        for client in Server.all_clients:
            mess = get_message(client.socket)
            if mess:
                name_from, name_to = get_names(mess)
                if not client.login:
                    client.login = name_from
                    print('client {} now has name'.format(client.login))
                mess['status'] = 'False'
                mongo_DB.add_message(mess)
                print('message {} was added to database'.format(mess))
        await asyncio.sleep(0.1)

async def WriteMessages():
    while True:
        for client in Server.all_clients:
        # for reader in Server.readers:
            message_list = mongo_DB.unsended_messages()
            if message_list:
                for unsended_message in message_list:
                    print('unsenden_message', unsended_message)
                    # s_actions.handler_unsended_mess(unsended_message, reader, Server.named_sockets)
                    s_actions.handler_unsended_mess(unsended_message, client)
                    # message_list=[]
        await asyncio.sleep(0.1)



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
            return mess or None
            # if not mess:
            #     return None
            # else:
            #     return mess


def lookup(mess):
    if 'user' in mess:
        return mess['user'].get('account_name')
    return mess.get('from')


def get_names(mess):
    name_from = lookup(mess)
    name_to = mess.get('to')
    return name_from, name_to

def mainloop(serv):
    eloop = asyncio.get_event_loop()
    tasks = [eloop.create_task(ChkClients(serv)), eloop.create_task(ReadMessages()), eloop.create_task(WriteMessages())]
    wait_tasks = asyncio.wait(tasks)
    eloop.run_until_complete(wait_tasks)




if __name__ == '__main__':
    server = Server()
    print('IP адрес сервера: ', server.IP)
    mainloop(server)

