import os
import sys

# Add the parent directory of the current file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import matplotlib.pyplot as plt
from bson import ObjectId
from flask import Flask, jsonify
from flask_cors import CORS
from config import settings
from database.connection import MongoDBConnection
from neural_network.neural_network import resize_images, insert_data, train_neural_network, read_data
from pymongo.errors import ConnectionFailure

app = Flask(__name__, static_url_path='/static', static_folder='public')
CORS(app)

@app.route('/train_neural_network')
def neural_network():
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

        # Generate the plot and save it to a file
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
        plt.title('My Plot')
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plot_dir = os.path.join(app.static_folder, 'plots')
        os.makedirs(plot_dir, exist_ok=True)  # Create the directory if it doesn't exist
        plot_path = os.path.join(plot_dir, 'my_plot.png')
        plt.savefig(plot_path)

        return "Neural network training completed successfully!"

    except ConnectionFailure as e:
        print("Failed to connect to MongoDB.")
        print(e)
        return "Failed to connect to MongoDB."

    # Finally close connection
    finally:
        if connection:
            connection.close()

# Data endpoint for fetching all data from database
@app.route('/data')
def get_data():
    connection = None
    db = None

    try:
        connection = MongoDBConnection(settings.DATABASE_URL)
        db = connection.get_database()

        # use the "db" object to interact with your MongoDB database

        print("Successfully connected to MongoDB!")
        print(f"Database URL: {settings.DATABASE_URL}")
        print(f"Database name: {settings.DATABASE_NAME}")

        # Get all the documents from the "woods" collection
        collection_name = 'woods'
        documents = db[collection_name].find()

        # Convert the ObjectId to string for all the documents
        data = []
        for doc in documents:
            doc['_id'] = str(doc['_id'])
            data.append(doc)

        return jsonify(data)

    except ConnectionFailure as e:
        print("Failed to connect to MongoDB.")
        print(e)
        return "Failed to connect to MongoDB."

    # Finally close connection
    finally:
        if connection:
            connection.close()

@app.route('/my_plot')
def my_plot():
    # Return the image file
    return app.send_static_file('plots/my_plot.png')

if __name__ == '__main__':
    app.run(debug=True)
