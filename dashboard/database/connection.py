from pymongo import MongoClient
from app import settings

class MongoDBConnection:
    def __init__(self, url):
        self.url = url
        self.client = MongoClient(self.url)

    def get_database(self):
        return self.client[settings.DATABASE_NAME]

    def close(self):
        self.client.close()

    def create_database_if_not_exists():
        connection = MongoClient(settings.DATABASE_URL)

        # check if the database exists
        database_names = connection.list_database_names()
        if settings.DATABASE_NAME not in database_names:
            # create the database
            connection[settings.DATABASE_NAME].command("create")
            print(f"Database '{settings.DATABASE_NAME}' created successfully!")
        else:
            # connect to the existing database
            db = connection[settings.DATABASE_NAME]
            print(f"Connected to database '{settings.DATABASE_NAME}'")

        connection.close()
