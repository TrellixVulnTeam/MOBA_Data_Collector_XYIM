import pymongo
import matplotlib
import pandas as pd
from elasticsearch import Elasticsearch


class Querying_Agent:
    def __init__(self, connector, database, collection):
        self.client = pymongo.MongoClient(connector)
        self.db = self.client[database]
        self.collection = self.db[collection]

        self.elastic = Elasticsearch(["http://localhost:9200"], verify_certs = True )
        self.index = self.elastic.index(index="players", id=None, body ={})

    def use_database(self, database):
        self.db = self.client[database]

    def use_collection(self, collection):
        self.collection = self.db[collection]

    def insert_record(self, records):
        self.collection.insert_one(records)

    def insert_bulk_csv(self, path):
        records = pd.read_csv(path).to_dict('records')
        self.collection.insert_many(records)

    def delete_records(self):
        self.collection.delete_many({})

    def find_one(self, attribute, value):
        print(self.collection.find_one({attribute:value}))

    def total(self):
        return self.collection.count_documents({})

    def top_X_Criteria(self, amount, criteria, data):
        ["Challenger", "Grandmaster", "Master", "Diamond", "Platinum", "Gold", "Silver", "Bronze", "Iron"]
        return list(self.collection.aggregate([
            {"$match": {criteria:data}},
            {"$sort":{"LP":1}},
            {"$limit":amount}
        ]))
        #return list(self.collection.find({criteria:data}).sort("LP", -1).limit(amount))