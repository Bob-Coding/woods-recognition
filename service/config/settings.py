import os
from dotenv import load_dotenv
load_dotenv()
API_URL = os.getenv("API_URL") or "http://localhost:5000"
MONGO_USERNAME= os.getenv("MONGO_USERNAME") or "root"
MONGO_PASSWORD= os.getenv("MONGO_PASSWORD") or "example"
DATABASE_URL= os.getenv("MONGO_URI") or f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/?authSource=admin" or "mongodb://root:example@localhost:27017/?authSource=admin"
DATABASE_NAME = os.getenv("DATABASE_NAME") or "woods_recognition"
DATABASE_URL = os.getenv("DATABASE_URL") or f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/{DATABASE_NAME}?authSource=admin"
COLLECTION_NAME = os.getenv("COLLECTION_NAME") or "dataset_cleaned"
TRAIN_DENSE_MODEL = os.getenv("TRAIN_DENSE_MODEL") or False
TRAIN_SEQ_DENSE_MODEL = os.getenv("TRAIN_SEQ_DENSE_MODEL") or False
IMAGES_PATH = os.getenv("IMAGES_PATH") or "./data/images/"
DATASET_PATH = os.getenv("DATASET_PATH") or "./data/dataset_cleaned.csv"
ENCODERS_MODEL_PATH = os.getenv("TARGET_PATH_NEW_MODEL") or "./data/"



