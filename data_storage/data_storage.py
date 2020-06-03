import pymongo

from config import config

client = pymongo.MongoClient(config.MONGO_DB_CLIENT)


def get_database():
    return client["movie_reviews"]


def get_column(name, db):
    return db[name]


def store_data(data):
    db = get_database()
    table = get_column('reviews', db)
    x = table.insert_many(data)

    print(x)
