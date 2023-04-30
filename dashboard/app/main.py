import os
import sys

# Add the parent directory of the current file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import settings
from database.connection import MongoDBConnection
from pymongo.errors import ConnectionFailure
from neural_network.neural_network import resize_images, read_data, insert_data, train_neural_network

connection = None
db = None

try:
    connection = MongoDBConnection(settings.DATABASE_URL)
    db = connection.get_database()

    # use the "db" object to interact with your MongoDB database

    print("Successfully connected to MongoDB!")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Database name: {settings.DATABASE_NAME}")

    # Resize images
    input_dir = '../data/images'
    output_dir = '../data/resized_images'
    size = 40
    images = resize_images(input_dir, output_dir, size)

    # Inserting data in the database
    file_path = '../data/data.csv'
    collection_name = 'woods'
    insert_data(collection_name, file_path, db)

    # Read data from the database
    data = read_data(file_path)

    # Inserting data in the database
    insert_data(collection_name, file_path, db)

    # Train the neural network
    train_neural_network(images, size)

except ConnectionFailure as e:
    print("Failed to connect to MongoDB.")
    print(e)

# Finally close connection
finally:
    if connection:
        connection.close()
