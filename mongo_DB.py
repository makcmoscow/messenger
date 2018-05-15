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
    user = found_user(login)
    if user:
        if str(user['login'])==str(login) and str(user['password']) == str(password):
            a = True
        elif str(user['login'])==str(login):
            a = False
        else:
            user = {'login': str(login), 'password': str(password)}
            users.insert_one(user)
            a = True
        return a
    else:
        user = {'login': str(login), 'password': str(password)}
        users.insert_one(user)
        a = ['user just added', True]#todo reaction if user doesn't exist in database

def found_user(login):
    for user in users.find({'login':str(login)}):
        print(user)
        return user
# users.insert_one({'login': 111, 'password': 111})
# autentification('111', 111)