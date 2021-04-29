import pymongo
import matplotlib
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

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
        records = pd.read_csv(path, keep_default_na=False).to_dict('records')
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
        sort = "Rank" if sort == None else sort
        way = 1 if sort == "Rank" else -1
        return list(self.collection.aggregate([
            {"$match": {criteria:data}},
            {"$sort":{sort:way}},
            {"$limit":amount}
        ]))

    def list(self):
        print(self.collection.distinct('Elo_Index'))

    def challengers_per_server(self):
        server = ['BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE', 'RU', 'TR']
        return [self.collection.find({"Server": s, "Elo":"Challenger"}).count() for s in server]


    #### ELASTIC ####

    def ping(self):
        self.elastic.ping()

    def delete_index(self, index):
        self.elastic.indices.delete(index=index)

    def data_to_dict(self, path):
        collection = pd.read_csv(path, keep_default_na=False)
        return collection.to_dict(orient="records")

    def index_collection(self, path):
        documents = self.data_to_dict(path)
        for docu in documents:
            yield {
                "_index": "players",
                "_source": {k: v for k, v in docu.items()},
            }

    def bulk_index(self, path):
        bulk(self.elastic, self.index_collection(path))

    def print_indexes(self):
        for index in self.elastic.indices.get('*'):
            print (index)

    def get_index(self, index):
        return self.elastic.get(index="players", id=index)

    def es_query(self):
        return self.elastic.count(index='players', doc_type='gamers')

    def search(self, size, name):
        return self.elastic.search(index="players", body={"from" : 0, "size" : size, "query": {"term":{"Name":name}}})
        #return self.elastic.search(index="players", body={"from" : 0, "size" : size, "query": {"term":{"Name":name}}})