from pymongo import MongoClient

client = MongoClient()
db = client.db
messages = db.messages
print(messages)

def add_message(message):
    messages.insert_one(message)
    print(messages.find())

