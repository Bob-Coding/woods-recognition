import os
import sys
import csv
from PIL import Image
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Add the parent directory of the current file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import settings
from database.connection import MongoDBConnection
from pymongo.errors import ConnectionFailure

# Function to resize images and return them as NumPy arrays
def resize_images(input_dir, output_dir, size):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    images = []
    for filename in os.listdir(input_dir):
        name, ext = os.path.splitext(filename)
        if ext == '.jpg':
            with Image.open(os.path.join(input_dir, filename)) as image:
                resized_image = image.resize((size, size))
                resized_image.save(os.path.join(output_dir, filename)) # save resized image
                np_image = np.array(resized_image) / 255.0 # convert to NumPy array
                images.append(np_image)
    return np.array(images)


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


    # Read data from CSV file
    with open('../data/data.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Insert data into MongoDB
    db.my_collection.insert_many(data)
    print("Data successfully inserted into MongoDB!")

    # Add target data
    target_data = np.random.randint(0, 10, (len(images), 10))

    # Split dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(images, target_data, test_size=0.2, random_state=42)

    # Train neural network
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(size, size, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=10)

    # Evaluate model on test set
    test_loss, test_acc = model.evaluate(X_test, y_test)
    print("Test accuracy:", test_acc)

    print("Neural network training completed successfully.")

    # Plot accuracy over time
    plt.plot(history.history['accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train'], loc='upper left')
    plt.show()

    # Determine the class predictions for the test set
    predictions = model.predict(X_test)
    class_predictions = np.argmax(predictions, axis=1)

    # Print the class predictions for the first 10 test images
    print("Class predictions for first 10 test images:")
    for i in range(10):
        print(f"Test image {i+1}: Class {class_predictions[i]}")

except ConnectionFailure as e:
    print("Failed to connect to MongoDB.")
    print(e)

# Finally close connection
finally:
    if connection:
        connection.close()