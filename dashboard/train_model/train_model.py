import csv
from PIL import Image
import pickle
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# Train model
def train():
    file_names = []
    labels = []

    with open('data/dataset_cleaned.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] != "_id":
                file_names.append(row[1])
                labels.append(row[2])

   
    mogelijke_labels_count = len(np.unique(labels))
    images = []
    encoded_labels = []
    label_encoder = LabelEncoder()

    for file_name, label in zip(file_names, labels):
        image = Image.open("data/images/" + file_name)
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
    with open('data/encoders.pkl', 'wb') as f:
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
    model.add(Dense(mogelijke_labels_count, activation='softmax'))

    # compile model
    optimizer = tf.keras.optimizers.Adam(learning_rate=best_learning_rate)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    # Train model
    model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_val, y_val))

    # Save trained model
    with open('data/getraind_model.pkl', 'wb') as file:
        pickle.dump(model, file)


