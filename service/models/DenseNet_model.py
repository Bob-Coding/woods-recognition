import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Conv2D, BatchNormalization, Activation, AveragePooling2D, GlobalAveragePooling2D, MaxPooling2D
from tensorflow.keras.regularizers import l2
from database.connection import MongoDBConnection
import seaborn as sns
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pickle
from config import settings
import csv
from bson.objectid import ObjectId

client = MongoDBConnection(settings.DATABASE_URL)
db = client.get_database()
collection = client.get_collection(settings.COLLECTION_NAME)

def train_dense_model():
    print("Training dense model...")
    file_names = []
    labels = []
    label_stats = {
        "Crack": {"correct_guesses": 0, "total_guesses": 0},
        "Dead_Knot": {"correct_guesses": 0, "total_guesses": 0},
        "Knot_Missing": {"correct_guesses": 0, "total_guesses": 0},
        "Knot_With_Crack": {"correct_guesses": 0, "total_guesses": 0},
        "Live_Knot": {"correct_guesses": 0, "total_guesses": 0},
        "Marrow": {"correct_guesses": 0, "total_guesses": 0},
        "Quartzity": {"correct_guesses": 0, "total_guesses": 0},
        "Resin": {"correct_guesses": 0, "total_guesses": 0},
        "clean": {"correct_guesses": 0, "total_guesses": 0},
    }

    with open('./data/dataset_cleaned.csv', 'r') as csvfile:
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

    possible_label_count = np.unique(labels)
    images = []
    encoded_labels = []
    label_encoder = LabelEncoder()

    for file_name, label in zip(file_names, labels):
        image = Image.open("./data/images/" + file_name)
        image = np.array(image)
        images.append(image)
        encoded_labels.append(label)

    possible_label_count = len(np.unique(labels))
    images = np.array(images)
    encoded_labels = np.array(encoded_labels)

    label_encoder.fit(encoded_labels)

    X_train, X_val_test, y_train, y_val_test = train_test_split(images, encoded_labels, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_val_test, y_val_test, test_size=0.5, random_state=42)

    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train)
    y_val = label_encoder.transform(y_val)

    y_test = label_encoder.transform(y_test)
    y_test = to_categorical(y_test)

    y_train = to_categorical(y_train)
    y_val = to_categorical(y_val)

    def dense_block(x, blocks, growth_rate):
        """Creëert een dense block met meerdere convolutional layers."""
        for _ in range(blocks):
            x = conv_block(x, growth_rate)
        return x

    def transition_block(x, reduction):
        """Creëert een transition block met een overgangsconvolutie en een pooling laag."""
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Conv2D(int(x.shape[-1] * reduction), kernel_size=1, padding='same', kernel_regularizer=l2(1e-4))(x)
        x = AveragePooling2D(pool_size=2, strides=2)(x)
        return x

    def conv_block(x, growth_rate):
        """Creëert een convolutional block met een batch normalization en een activation laag."""
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Conv2D(growth_rate, kernel_size=3, padding='same', kernel_regularizer=l2(1e-4))(x)
        return x

    def create_densenet(input_shape, num_classes, blocks_per_group, growth_rate):
        """Creëert een DenseNet model met de gegeven parameters."""
        # Input laag
        inputs = Input(shape=input_shape)
        x = Conv2D(64, kernel_size=7, strides=2, padding='same', kernel_regularizer=l2(1e-4))(inputs)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = MaxPooling2D(pool_size=3, strides=2, padding='same')(x)

        # Dense blocks
        for blocks in blocks_per_group:
            x = dense_block(x, blocks, growth_rate)
            x = transition_block(x, 0.5)

        # Last layer
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = GlobalAveragePooling2D()(x)
        x = Dense(num_classes, activation='softmax')(x)

        # make model
        model = Model(inputs, x, name='densenet')
        return model

    # Define params DenseNet
    input_shape = (256, 700, 3)  
    num_classes = possible_label_count  
    blocks_per_group = [6, 12, 24, 16]  
    growth_rate = 32  

    # Create DenseNet model
    model = create_densenet(input_shape, num_classes, blocks_per_group, growth_rate)

    # Compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # Train model
    model.fit(X_train, y_train, batch_size=32, epochs=30, validation_data=(X_val, y_val))

    y_pred = model.predict(X_val)

    # Evaluate model
    test_loss, test_accuracy = model.evaluate(X_test, y_test)

    # Convert one-hot encoded y_test to multiclass format
    y_test_multiclass = np.argmax(y_test, axis=1)

    # Convert predictions to integer labels
    y_pred_labels = np.argmax(y_pred, axis=1)

    # Calculate the confusion matrix
    cm = confusion_matrix(y_test_multiclass, y_pred_labels)

    # Update label_stats with correct_guesses
    for i in range(len(y_test_multiclass)):
        true_label = y_test_multiclass[i]
        predicted_label = y_pred[i]

        if true_label == np.argmax(predicted_label):
            label = label_encoder.inverse_transform([np.argmax(predicted_label)])[0]
            label_stats[label]['correct_guesses'] += 1

        # Increment total_guesses for the predicted label
        label_stats[label]['total_guesses'] += 1

    # Save label_stats dictionary
    with open(settings.ENCODERS_MODEL_PATH + 'label_stats_dense.pkl', 'wb') as f:
        pickle.dump(label_stats, f)

    cm_folder = os.path.join("./app/static", "cm")
    os.makedirs(os.path.join(cm_folder), exist_ok=True)

    # Plot confusion matrix with seaborn
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel('Predicted labels')
    plt.ylabel('True labels')
    plt.title('Confusion Matrix')
    plt.savefig(cm_folder + '/densenet_confusion_matrix.png')

    # save encoder
    with open(settings.ENCODERS_MODEL_PATH + 'dense_encoder.pkl', 'wb') as file:
        pickle.dump(label_encoder, file)
    # Save trained model
    with open(settings.ENCODERS_MODEL_PATH + 'dense_trained_model.pkl', 'wb') as file:
        pickle.dump(model, file)
