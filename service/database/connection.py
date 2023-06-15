import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import settings
from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, url):
        self.url = url
        print(self.url)
        self.client = MongoClient(self.url)

    def get_collection(self, collection_name):
        if self.client is None:
            self.client = MongoClient(self.url)
    
        db = self.client[settings.DATABASE_NAME]
        collection_names = db.list_collection_names()
        if collection_name not in collection_names:
            # Collection does not exist, create it
            db.create_collection(collection_name)
    
        return db[collection_name]

    def close(self):
        self.client.close()
        self.client = None

    def get_database(self):
        if self.client is None:
            self.client = MongoClient(self.url)
        
        db = self.client[settings.DATABASE_NAME]
        return db

        
