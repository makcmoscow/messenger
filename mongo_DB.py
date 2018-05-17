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
    messages.update({'_id':id}, {'$set':{'status':'True'}})

def autentication(login, password):
    user = found_user(login)
    if user:
        if user['login']==login and user['password'] == password:
            a = True
        elif user['login']==login:
            a = False
        return a
    else:
        user = {'login': login, 'password': password}
        users.insert_one(user)
        a = True#todo reaction if user doesn't exist in database
        return a

def found_user(login):
    for user in users.find({'login':login}):
        print(user)
        return user

def show_users():
    for user in users.find({}):
        print(user)

def show_messages():
    for message in messages.find({}):
        print(message)



if __name__ == '__main__':
    show_messages()


    # mes = messages.find({'status':'True'})
    # for message in mes:
    #     print(message)
        # messages.remove(message)
        # print('{} removed'.format(message))




# users.insert_one({'login': 111, 'password': 111})
# autentification('111', 111)