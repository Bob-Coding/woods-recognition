import os
import sys
import csv

# Add the parent directory of the current file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    # Read data from CSV file
    with open('../data/data.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Insert data into MongoDB
    db.woods.insert_many(data)
    print("Data successfully inserted into MongoDB!")

except ConnectionFailure as e:
    print("Failed to connect to MongoDB.")
    print(e)

# Finally close connection
finally:
    if connection:
        connection.close()
