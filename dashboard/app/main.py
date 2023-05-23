import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings
from database.connection import MongoDBConnection
from train_model.train_model import train
import pickle
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger
from tensorflow.keras.preprocessing import image

if settings.TRAIN_MODEL == True:
    train()

app = Flask(__name__)
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
def check_file():
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
    data = request.get_json()
    filename = data['path']
    if os.path.exists(filename):
        
        # Laden van het getrainde model
        with open('./data/getraind_model.pkl', 'rb') as f:
            model = pickle.load(f)

        # Laden van de opgeslagen encoders en encoded_labels
        with open('./data/encoders.pkl', 'rb') as f:
            loaded_encoders = pickle.load(f)

        label_encoder = loaded_encoders['label_encoder']

        # Laad het plaatje
        img_path = filename
        print(img_path)
        img = image.load_img(img_path, target_size=(256, 700))  # Pas de doelgrootte aan op basis van je model

        # Converteer het plaatje naar een Numpy-array
        img_array = image.img_to_array(img)

        # Breid de dimensie uit, omdat het model meestal batches van afbeeldingen verwacht
        img_array = np.expand_dims(img_array, axis=0)

        # Doe de voorspelling met behulp van het geladen model
        predictions = model.predict(img_array)

        # Decodeer de voorspellingen naar leesbare labels
        decoded_predictions = label_encoder.inverse_transform(np.argmax(predictions, axis=1))

        # Decodeer ook de mogelijke gokken van het model
        decoded_possible_labels = label_encoder.inverse_transform(np.argsort(-predictions, axis=1)[:, :3].ravel())

        # Plot het voorspelde label
        fig, ax = plt.subplots()
        ax.bar(decoded_predictions, np.max(predictions, axis=1))
        ax.set_xlabel('Label')
        ax.set_ylabel('Voorspelde waarde')
        ax.set_title('Voorspeld label')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('app/public/plots/voorspeld_label.png')
        plt.close()

        # Plot de mogelijke gokken van het model
        fig, ax = plt.subplots()
        ax.bar(decoded_possible_labels.ravel(), predictions.ravel()[np.argsort(-predictions, axis=1)[:, :3]].ravel())
        ax.set_xlabel('Label')
        ax.set_ylabel('Voorspelde waarde')
        ax.set_title('Mogelijke gokken van het model')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('app/public/plots/mogelijke_gokken.png')
        plt.close()
        return "done"
            
    else:
        return jsonify({'message': 'File does not exist'}), 404

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
