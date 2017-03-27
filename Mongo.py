#!/usr/bin/python
# -*- encoding: utf-8 -*-

# Work on python 2.7
# Need: pymongo

import pymongo

class Mongo:
    def __init__(self, dbhost='localhost', port=27017, dbname='admin'):
        self.client = pymongo.MongoClient(dbhost,port)
        self.db = self.client[dbname]

    def insert(self, collection, data):
        t = self.db[collection]
        t.insert_one(data).inserted_id

    def find(self, collection, condition=None):
        t = self.db[collection]
        if condition is None:
            return t.find()
        else:
            return t.find(condition)

    def update(self, table, collection):
        t = self.db[table]

    def __repr__(self):
        self.client.close()

if __name__ == '__main__':
    pass