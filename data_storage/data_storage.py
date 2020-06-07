import pymongo

from config import config


class Database:

    def __int__(self):
        pass

    @staticmethod
    def get_connection():
        return pymongo.MongoClient(config.MONGO_DB_CLIENT)

    def store_data(self, table_name, data):
        with self.get_connection() as client:
            _db = client[config.SCHEMA_NAME]
            table = _db[table_name]
            table.insert_many(data)
