import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings
from database.connection import MongoDBConnection
from models.Seq_DenseNet_model import train
import pickle
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

if not os.path.exists(settings.ENCODERS_MODEL_PATH + 'encoders.pkl') or (not os.path.exists(settings.ENCODERS_MODEL_PATH + 'seq_trained_model.pkl') and not os.path.exists(settings.ENCODERS_MODEL_PATH + 'seq_dense_trained_model.pkl')) or settings.TRAIN_MODEL == True:
  train()

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})

client = MongoDBConnection(settings.DATABASE_URL)
db = client.get_database()
collection = client.get_collection(settings.COLLECTION_NAME)

@app.route('/plots', methods=['GET'])
def get_items():
    """
    Get all items
    ---
    tags:
    - Items
    responses:
      200:
        description: OK
    """
    items = list(collection.find({}))
    return jsonify(items)

@app.route("/classify_image", methods=["POST"])
@cross_origin(origin='*', headers=['Content-Type'])
def classify():
    """
    Classify an uploaded image to a specific label
    ---
    tags:
    - Items
    parameters:
      - name: filename
        in: body
        required: true
        schema:
          type: object
    responses:
      200:
        description: OK
    """
    with open(settings.ENCODERS_MODEL_PATH + 'seq_trained_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open(settings.ENCODERS_MODEL_PATH + 'encoders.pkl', 'rb') as f:
        loaded_encoders = pickle.load(f)
    label_encoder = loaded_encoders['label_encoder']

    image_files = request.files.getlist('imageFiles')
    
    # clean old images and plots
    images_folder = os.path.join(app.static_folder, "received_images")
    plots_folder = os.path.join(app.static_folder, "plots")
    
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
        plot_filepath_1 = f'{os.path.join(app.static_folder, "plots", os.path.splitext(filename)[0])}-label.png'
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
        plot_filepath_2 = f'{os.path.join(app.static_folder,"plots", os.path.splitext(filename)[0])}-labels.png'
        plt.savefig(plot_filepath_2)
        plt.close()
        plot_urls.append(f'{settings.API_URL}/static/plots/{os.path.splitext(filename)[0]}-labels.png')
        response.append({filename: plot_urls})
    return jsonify(response)
  
@app.route('/items', methods=['POST'])
def add_item():
    """
    Add a new item
    ---
    tags:
    - Items
    parameters:
      - name: item
        in: body
        required: true
        schema:
          type: object
    responses:
      200:
        description: OK
    """
    data = request.get_json()
    collection.insert_one(data)
    return jsonify({'message': 'Item added successfully'})


@app.route('/voorspeld_label')
def my_plot_label():
    # Return the image file
    return app.send_static_file('plots/voorspeld_label.png')

@app.route('/mogelijke_gokken')
def my_plot_gokken():
    # Return the image file
    return app.send_static_file('plots/mogelijke_gokken.png')


@app.route('/preprocess_data', methods=['POST'])
def preprocess_data():
    """
    Preprocesses the data for training the model.
    ---
    parameters:
      - name: subset_size
        in: query
        type: integer
        description: Number of images to include in the subset
        required: true
    responses:
      200:
        description: Preprocessing completed successfully
    """
# Generate Swagger API definition
@app.route('/swagger.json', methods=['GET'])
def swagger_json():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "  API"
    return jsonify(swag)

# Add the Swagger UI route
SWAGGER_URL = '/docs'
API_URL = '/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,config={
    'app_name': "Your API Title"
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)
