from pymongo import MongoClient

client = MongoClient()
db = client.db
messages = db.messages


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
