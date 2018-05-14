from pymongo import MongoClient

client = MongoClient()
db = client.database
messages = db.messages


def add_message(message):
    messages.insert_one(message)
    print(messages.find())

