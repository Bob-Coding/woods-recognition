from config import settings
from database.connection import MongoDBConnection
from pymongo.errors import ConnectionFailure

try:
    connection = MongoDBConnection(settings.DATABASE_URL)
    db = connection.get_database()

    # use the "db" object to interact with your MongoDB database

    print("Successfully connected to MongoDB!")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Database name: {settings.DATABASE_NAME}")
except ConnectionFailure as e:
    print("Failed to connect to MongoDB.")
    print(e)
finally:
    if connection:
        connection.close()
