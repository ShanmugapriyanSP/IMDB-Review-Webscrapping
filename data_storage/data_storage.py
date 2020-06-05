import pymongo

from config import config

client = pymongo.MongoClient(config.MONGO_DB_CLIENT)


def get_database():
    return client[config.SCHEMA_NAME]


def get_table(name, db):
    return db[name]


def store_data(data, table_name):
    db = get_database()
    table = get_table(table_name, db)
    x = table.insert_many(data)

    print(x)
