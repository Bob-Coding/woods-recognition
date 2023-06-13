import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings
import pickle
from database.connection import MongoDBConnection
from models.train import train_model, classify_image
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger import swagger

if settings.TRAIN_DENSE_MODEL == "True":
    train_model('dense_model')
if settings.TRAIN_SEQ_DENSE_MODEL == "True":
    train_model('seq_dense_model')

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
    model = request.form.get('modelType')
    response = classify_image(model)
    return response

@app.route('/bubble_chart', methods=['GET'])
def get_bubble_chart_data():
    # Open en laad de gegevens van het pkl-bestand
    with open(settings.ENCODERS_MODEL_PATH + 'label_stats_seq_dense.pkl', 'rb') as file:
        bubble_data = pickle.load(file)
    return jsonify(bubble_data)
  
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
