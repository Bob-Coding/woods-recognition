import os
from dotenv import load_dotenv
load_dotenv()

USERNAME= os.getenv("USERNAME") or "root"
PASSWORD= os.getenv("PASSWORD") or "example"
DATABASE_NAME = os.getenv("DATABASE_NAME") or "big_data"
DATABASE_URL = os.getenv("DATABASE_URL") or f"mongodb://{USERNAME}:{PASSWORD}@localhost:27017/{DATABASE_NAME}?authSource=admin"
COLLECTION_NAME = os.getenv("COLLECTION_NAME") or "dataset_cleaned"
TRAIN_MODEL = os.getenv("TRAIN_MODEL") or False

