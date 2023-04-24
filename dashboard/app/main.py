# Add the parent directory of the current file to the Python path
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import settings
import csv
from PIL import Image, ImageOps

from database.connection import MongoDBConnection
from pymongo.errors import ConnectionFailure
import pandas as pd

try:
    connection = MongoDBConnection(settings.DATABASE_URL)
    db = connection.get_database()

    # use the "db" object to interact with your MongoDB database

    print("Successfully connected to MongoDB!")
    print(f"Database URL: {settings.DATABASE_URL}")
    print(f"Database name: {settings.DATABASE_NAME}")

    # Read data from CSV file
    dfhotel = pd.read_csv('../data/data.csv')

    with open('../data/data.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

    # Insert data into MongoDB
    db.woods.insert_many(data)
    print("Data successfully inserted into MongoDB!")


    # Resize images
    # Stel de grootte in waarnaar de afbeeldingen moeten worden geresized
    size = (60, 60)

    # Loop door alle afbeeldingen in een map
    for filename in os.listdir('../data/images'):
        # Controleer of het bestand een afbeelding is
        if filename.endswith('.jpg'):
            # Open de afbeelding
            with Image.open('../data/images/' + filename) as img:

                # bepaal de gewenste afmetingen
                target_width = 40
                target_height = 40

                # bereken de middelpunten
                width, height = img.size
                left = (width - target_width) / 2
                top = (height - target_height) / 2
                right = (width + target_width) / 2
                bottom = (height + target_height) / 2

                # bijsnijden en opslaan
                img_path = '../data/images/resized/'
                if not os.path.exists(img_path):
                    os.mkdir(img_path)

                # controleer of de afbeelding kleiner is dan de gewenste afmetingen
                if width < target_width or height < target_height:
                    # bereken de padding om toe te voegen
                    horizontal_padding = max(target_width - img.width, 0) // 2
                    vertical_padding = max(target_height - img.height, 0) // 2

                    # voeg de padding toe en sla op
                    img_padded = ImageOps.expand(img, border=(horizontal_padding, vertical_padding), fill="white")
                    img_padded.save(img_path + filename)
                else:
                    # bijsnijden en opslaan
                    img_cropped = img.crop((left, top, right, bottom))
                    img_cropped.save(img_path + filename)


                # # Pas de grootte van de afbeelding aan
                # img_resized = img.resize(size)
                # # Sla de aangepaste afbeelding op met een andere bestandsnaam
                # if not os.path.exists(img_path):
                #     os.mkdir(img_path)
                # img_resized.save(img_path + filename)
    print("Pictures resized to " + str(size))

except ConnectionFailure as e:
    print("Failed to connect to MongoDB.")
    print(e)

# Finally close connection
finally:
    if connection:
        connection.close()
