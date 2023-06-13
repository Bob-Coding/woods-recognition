import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings
from models.Seq_DenseNet_model import train_seq_dense_model
from models.DenseNet_model import train_dense_model
import pickle
import matplotlib.pyplot as plt
import numpy as np
from flask import request, jsonify
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

def train_model(model):
    if model == "seq_dense_model":
        train_seq_dense_model()
    elif model == "dense_model":
        train_dense_model()
    else:
        print("Model not found")
        return
    
def classify_image(model):
    if model == "Sequential DenseNet Model":
        with open(settings.ENCODERS_MODEL_PATH + 'seq_dense_trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open(settings.ENCODERS_MODEL_PATH + 'seq_dense_encoders.pkl', 'rb') as f:
            loaded_encoders = pickle.load(f)
        label_encoder = loaded_encoders['label_encoder']
    elif model == "DenseNet Model":
        with open(settings.ENCODERS_MODEL_PATH + 'dense_trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open(settings.ENCODERS_MODEL_PATH + 'dense_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
    else:
        print("Model not found")
        return

    image_files = request.files.getlist('imageFiles')
    
    # clean old images and plots
    images_folder = os.path.join("./app/static", "received_images")
    plots_folder = os.path.join("./app/static", "plots")
    
    if(os.path.exists(images_folder)):
        for image_name in os.listdir(images_folder):
            file_path = os.path.join(images_folder, image_name)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))    
    if(os.path.exists(plots_folder)):
            for plot_name in os.listdir(plots_folder):
                file_path = os.path.join(plots_folder, plot_name)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))    
      
    # Create folder for saving images and plots
    os.makedirs(images_folder, exist_ok=True)
    os.makedirs(plots_folder, exist_ok=True)
    
    response = []

    for image_file in image_files:
        plot_urls = []
        filename = secure_filename(image_file.filename)
        static_filepath = os.path.join(images_folder, filename)
        image_file.save(static_filepath)
        
        img = image.load_img(static_filepath, target_size=(256, 700))  # Pas de doelgrootte aan op basis van je model
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        
        predictions = model.predict(img_array)

        decoded_predictions = label_encoder.inverse_transform(np.argmax(predictions, axis=1))
        decoded_possible_labels = label_encoder.inverse_transform(np.argsort(-predictions, axis=1)[:, :3].ravel())
        
        # Plot possible label top 1 pick
        fig, ax = plt.subplots()
        ax.bar(decoded_predictions, np.max(predictions, axis=1))
        ax.set_xlabel('Label')
        ax.set_ylabel('Voorspelde waarde')
        ax.set_title('Voorspeld label')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot_filepath_1 = f'{os.path.join("./app/static", "plots", os.path.splitext(filename)[0])}-label.png'
        plt.savefig(plot_filepath_1)
        plt.close()
        plot_urls.append(f'{settings.API_URL}/static/plots/{os.path.splitext(filename)[0]}-label.png')

        # Plot possible labels top 3 picks
        fig, ax = plt.subplots()
        ax.bar(decoded_possible_labels.ravel(), predictions.ravel()[np.argsort(-predictions, axis=1)[:, :3]].ravel())
        ax.set_xlabel('Label')
        ax.set_ylabel('Voorspelde waarde')
        ax.set_title('Mogelijke gokken van het model')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot_filepath_2 = f'{os.path.join("./app/static","plots", os.path.splitext(filename)[0])}-labels.png'
        plt.savefig(plot_filepath_2)
        plt.close()
        plot_urls.append(f'{settings.API_URL}/static/plots/{os.path.splitext(filename)[0]}-labels.png')
        response.append({filename: plot_urls})
    return jsonify(response)