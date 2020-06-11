"""
Mongo db operations
"""
import pymongo

import config


class Database:
    """
    Class for Database operations
    """

    def __int__(self):
        pass

    @staticmethod
    def get_connection():
        """
        To connect with mongo db client
        """
        return pymongo.MongoClient(config.MONGO_DB_CLIENT)

    def store_data(self, table_name, data):
        """
        Store data as dict
        """
        with self.get_connection() as client:
            _db = client[config.SCHEMA_NAME]
            table = _db[table_name]
            _id = table.insert_many(data)
            print(_id)

    def store_data_with_list_of_list(self, table_name, data):
        """
        Storing list of list of dicts
        """
        with self.get_connection() as client:
            _db = client[config.SCHEMA_NAME]
            table = _db[table_name]
            for dict_list in data:
                _id = table.insert_many(dict_list)
                print(_id)

    def retrieve_data(self, table_name):
        """
        To get data from a table
        """
        with self.get_connection() as client:
            _db = client[config.SCHEMA_NAME]
            table = _db[table_name]
            result = list(table.find())
        return result
