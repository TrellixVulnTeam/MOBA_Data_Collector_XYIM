import pymongo

class Mongo_Client:
    def __init__(self, connector, database, collection):
        self.client = pymongo.MongoClient(connector)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def use_database(self, database):
        self.db = self.client[database]

    def use_collection(self, collection):
        self.collection = self.db[collection]

    def insert_record(self, records):
        self.collection.insert_one(records)

    def insert_bulk(self, records):
        self.collection.insert_many(records)

    def delete_records(self):
        self.collection.delete_many({})

    def find_one(self, attribute, value):
        print(self.collection.find_one({attribute:value}))