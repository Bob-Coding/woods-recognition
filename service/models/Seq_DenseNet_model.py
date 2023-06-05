import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings
import csv
from PIL import Image
import pickle
import numpy as np
from database.connection import MongoDBConnection
from bson.objectid import ObjectId
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

client = MongoDBConnection(settings.DATABASE_URL)
db = client.get_database()
collection = client.get_collection(settings.COLLECTION_NAME)

# Train model
def train_seq_dense_model():
    print("Training seq dense model...")
    file_names = []
    labels = []

    with open(settings.DATASET_PATH, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] != "_id":
                file_names.append(row[1])
                labels.append(row[2])
                # create document for mongoDB
                document = {
                    'file': row[1],
                    'label': row[2]
                }

                # Check if document exists
                existing_document = collection.find_one({'file': row[1]})

                if existing_document:
                    # Update document
                    existing_document['label'] = row[2]

                    # Save document
                    collection.update_one({'file': row[1]}, {'$set': {'label': row[2]}})
                else:
                    # create new document with generated ID
                    document = {
                    '_id': ObjectId(),
                    'file': row[1],
                    'label': row[2]
                    }   

                    # Insert document
                    collection.insert_one(document)
    client.close()
   
    possible_labels_count = len(np.unique(labels))
    images = []
    encoded_labels = []
    label_encoder = LabelEncoder()

    for file_name, label in zip(file_names, labels):
        image = Image.open(settings.IMAGES_PATH + file_name)
        image = np.array(image)
        images.append(image)
        encoded_labels.append(label)

    images = np.array(images)
    encoded_labels = np.array(encoded_labels)

    label_encoder.fit(encoded_labels)

    # Transform labels to numeric labels
    encoded_labels_numeric = label_encoder.transform(encoded_labels)

    # One-hot encoding labels
    onehot_encoder = OneHotEncoder(sparse=False)
    encoded_labels_onehot = onehot_encoder.fit_transform(encoded_labels_numeric.reshape(-1, 1))

    # Save LabelEncoder, OneHotEncoder, encoded_labels 
    encoders = {'label_encoder': label_encoder, 'onehot_encoder': onehot_encoder, 'encoded_labels': encoded_labels}
    with open(settings.ENCODERS_MODEL_PATH + 'seq_dense_encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)

    # Split set in trainings set and test set 
    X_train, X_val_test, y_train, y_val_test = train_test_split(images, encoded_labels_onehot, test_size=0.2, random_state=42)

    # Split test set in validation and test set
    X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=42)

    # get best params
    best_learning_rate = 0.001
    best_dropout_rate = 0.8
    best_filter_size = 3
    best_num_filters = 32
    best_num_layers = 1

    # define model
    model = Sequential()

    # add layers
    model.add(Conv2D(best_num_filters, (best_filter_size, best_filter_size), activation='relu', input_shape=(256, 700, 3)))
    model.add(MaxPooling2D((2, 2)))

    for _ in range(best_num_layers):
        model.add(Conv2D(best_num_filters, (best_filter_size, best_filter_size), activation='relu'))
        model.add(MaxPooling2D((2, 2)))

        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(best_dropout_rate))
        model.add(Dense(possible_labels_count, activation='softmax'))

        # compile model
        optimizer = Adam(learning_rate=best_learning_rate)
        model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

        # Train model
        model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_val, y_val))

        # Generate predictions for the test data
        y_pred = model.predict(X_test)
        y_pred = np.argmax(y_pred, axis=1)

        # Convert one-hot encoded y_test to multiclass format
        y_test_multiclass = np.argmax(y_test, axis=1)

        # Calculate the confusion matrix
        cm = confusion_matrix(y_test_multiclass, y_pred)

        cm_folder = os.path.join("./app/static", "cm")
        os.makedirs(os.path.join(cm_folder), exist_ok=True)
        
        # Plot the confusion matrix using seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.xlabel('Predicted labels')
        plt.ylabel('True labels')
        plt.title('Confusion Matrix')
        plt.savefig(cm_folder + '/seq_confusion_matrix.png')

        # Save trained model
        with open(settings.ENCODERS_MODEL_PATH + 'seq_trained_model.pkl', 'wb') as file:
            pickle.dump(model, file)

