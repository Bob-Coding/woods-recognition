import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import settings
from pymongo import MongoClient


class MongoDBConnection:
    def __init__(self, url):
        self.url = url
        self.client = MongoClient(self.url)

    def get_database(self):
        if self.client is None:
            self.client = MongoClient(self.url)
        return self.client[settings.DATABASE_NAME]
    
    def get_collection(self, collection_name):
        if self.client is None:
            self.client = MongoClient(self.url)
        return self.client[settings.DATABASE_NAME][collection_name]

    def close(self):
        self.client.close()
        self.client = None

    def create_database_if_not_exists(self):
        # check if the database exists
        database_names = self.client.list_database_names()
        if settings.DATABASE_NAME not in database_names:
            # create the database
            self.client[settings.DATABASE_NAME].command("create")
        return self.client[settings.DATABASE_NAME]

        
