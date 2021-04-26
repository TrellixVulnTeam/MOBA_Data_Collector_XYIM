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

    def rename(self, previous, new):
        self.collection.update({}, {"$rename":{previous:new}}, False, True)

    #["Challenger", "Grandmaster", "Master", "Diamond", "Platinum", "Gold", "Silver", "Bronze", "Iron"]
    def top_X_Criteria(self, amount, criteria, data, sort):
        way = 1 if sort == "Rank" else -1
        return list(self.collection.aggregate([
            {"$match": {criteria:data}},
            {"$sort":{sort:way}},
            {"$limit":amount}
        ]))

    def list(self):
        print(self.collection.distinct('Elo_Index'))

    def update_elo_index(self):
        self.collection.update({}, {"$set": {"Elo_Index": "0"}}, False, True)
        #self.collection.update({Elo: "Challenger"}, {"$set": {Elo_Index: 0}}, {multi: true})
        self.collection.update({"Elo": "Grandmaster"}, {"$set": {"Elo_Index": "1"}}, True)
        self.collection.update({"Elo": "Master"}, {"$set": {"Elo_Index": "2"}}, True)
        self.collection.update({"Elo": "Diamond"}, {"$set": {"Elo_Index": "3"}}, True)
        self.collection.update({"Elo": "Platinum"}, {"$set": {"Elo_Index": "4"}}, True)
        self.collection.update({"Elo": "Gold"}, {"$set": {"Elo_Index": "5"}}, True)
        self.collection.update({"Elo": "Silver"}, {"$set": {"Elo_Index": "6"}}, True)
        self.collection.update({"Elo": "Bronze"}, {"$set": {"Elo_Index": "7"}}, True)
        self.collection.update({"Elo": "Iron"}, {"$set": {"Elo_Index": "8"}}, True)