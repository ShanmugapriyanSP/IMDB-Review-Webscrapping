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
            x = table.insert_many(data)
            print(x)

    def store_data_with_list_of_list(self, table_name, data):
        with self.get_connection() as client:
            _db = client[config.SCHEMA_NAME]
            table = _db[table_name]
            for dict_list in data:
                x = table.insert_many(dict_list)
                print(x)

    def retrieve_data(self, table_name):
        with self.get_connection() as client:
            _db = client[config.SCHEMA_NAME]
            table = _db[table_name]
            result = list(table.find())
        return result
