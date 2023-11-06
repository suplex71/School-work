
from Credentials import storecreds as cfg
from pymongo import MongoClient

class MongoDBReader:
    def __init__(self):
        self.client = MongoClient(cfg.mongo_database["myclient"])
        self.database = self.client[cfg.mongo_database["mydb"]]

    def read_tickets(self):
        try:
            collection = self.database[cfg.mongo_database["mycol"]]
            data = collection.find()
            print(data)
            data_list = []
            for document in data:
                data_list.append(dict(document))
            return data_list
        except Exception as e:
            data=["Error"]
            return data

    def disconnect(self):
        self.client.close()