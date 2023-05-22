import os
import sys
from PIL import Image
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
import pickle
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# Add the parent directory of the current file to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv


# Haal de bestandsnamen en labels op
def train():
    file_names = []
    labels = []

    with open('./data/dataset_cleaned.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] != "_id":
                file_names.append(row[1])
                labels.append(row[2])

    # Aantal afbeeldingen dat je wilt gebruiken (subset grootte)
    subset_size = 4000

    # Selecteer een subset van de bestandsnamen en labels
    # file_names_subset = file_names[-subset_size:]
    # labels_subset = labels[-subset_size:]
    # mogelijke labels
    mogelijke_labels_count = len(np.unique(labels))
    print(mogelijke_labels_count)
    # Laden van afbeeldingen en coderen van labels
    images = []
    encoded_labels = []
    # Definieer en pas de labelencoder toe
    label_encoder = LabelEncoder()

    for file_name, label in zip(file_names, labels):
        # Laden van afbeelding
        image = Image.open("./data" + file_name)
        # image = image.resize((700, 256))  # Resizen naar gewenste dimensies

        image = np.array(image)

        # Toevoegen aan de lijst van afbeeldingen
        images.append(image)
        # Coderen van labels
        encoded_labels.append(label)

    # Omzetten naar Numpy-arrays
    images = np.array(images)
    encoded_labels = np.array(encoded_labels)

    # Fitten van de LabelEncoder op de labels
    label_encoder.fit(encoded_labels)

    # Transformeren van de labels naar numerieke waarden
    encoded_labels_numeric = label_encoder.transform(encoded_labels)

    # One-hot encoderen van de labels
    onehot_encoder = OneHotEncoder(sparse=False)
    encoded_labels_onehot = onehot_encoder.fit_transform(encoded_labels_numeric.reshape(-1, 1))

    # Sla de LabelEncoder, OneHotEncoder en encoded_labels op
    encoders = {'label_encoder': label_encoder, 'onehot_encoder': onehot_encoder, 'encoded_labels': encoded_labels}
    with open('encoders.pkl', 'wb') as f:
        pickle.dump(encoders, f)


    # Split de dataset in trainingsset en tijdelijke set (voor verder splitsen in validatie- en testset)
    X_train, X_val_test, y_train, y_val_test = train_test_split(images, encoded_labels_onehot, test_size=0.2, random_state=42)

    # Split de tijdelijke set in validatieset en testset
    X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=42)


    # Controleren van de verdeling van de gegevens
    print("Aantal trainingsvoorbeelden:", X_train.shape[0])
    print("Aantal testvoorbeelden:", X_test.shape[0])

    # Beste parameters ophalen
    best_learning_rate = 0.001
    best_dropout_rate = 0.8
    best_filter_size = 3
    best_num_filters = 32
    best_num_layers = 1

    # Definieer het model
    model = Sequential()

    # Voeg de lagen toe aan het model
    model.add(Conv2D(best_num_filters, (best_filter_size, best_filter_size), activation='relu', input_shape=(256, 700, 3)))
    model.add(MaxPooling2D((2, 2)))

    for _ in range(best_num_layers):
        model.add(Conv2D(best_num_filters, (best_filter_size, best_filter_size), activation='relu'))
        model.add(MaxPooling2D((2, 2)))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(best_dropout_rate))
    model.add(Dense(mogelijke_labels_count, activation='softmax'))

    # Compileer het model met de beste leersnelheid
    optimizer = tf.keras.optimizers.Adam(learning_rate=best_learning_rate)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    # Train het model
    model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_val, y_val))

    # Evalueren van het model op de testset
    test_loss, test_accuracy = model.evaluate(X_test, y_test)
    print(f"Test Loss: {test_loss}")
    print(f"Test Accuracy: {test_accuracy}")

    # Opslaan van het getrainde model
    with open('/content/drive/MyDrive/getraind_model2.pkl', 'wb') as file:
        pickle.dump(model, file)


