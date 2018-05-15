from pymongo import MongoClient

client = MongoClient()
db = client.db
messages = db.messages
users = db.users


def add_message(message):
    messages.insert_one(message)


def unsended_messages():
    message_list = []
    for message in messages.find({'status':'False'}):
        message_list.append(message)
        return message_list

def update_sended(sended_message):
    id = sended_message['_id']
    messages.update({'_id':id}, {'status':'True'})

def autentification(login, password):
    for user in users.find(): #{'name':login}
        if str(user['login'])==str(login) and str(user['password']) == str(password):
            a = ['login and password ok', True]
        elif str(user['login'])==str(login):
            a = ['Incorrect password', False]
        else:
            user = {'login': str(login), 'password': str(password)}
            users.insert_one(user)
            a = ['user just added', True]
        return a
# users.insert_one({'login': 111, 'password': 111})
# autentification('111', 111)