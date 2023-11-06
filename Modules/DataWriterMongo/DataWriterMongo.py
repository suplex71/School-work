import pymongo
from Credentials import storecreds as cfg

from pymongo import MongoClient

class DataWriterMongo:
    def __init__(self):
        self.client = MongoClient(cfg.mongo_database["myclient"])
        self.database = self.client[cfg.mongo_database["mydb"]]

    def insert_ticket(self, data):
        collection = self.database[cfg.mongo_database["mycol"]]
        collection.insert_many(data)

    def close_connection(self):
        self.client.close()