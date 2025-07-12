from pymongo import MongoClient
from datetime import datetime
client = MongoClient("mongodb://localhost:27017/")  
db = client['plant_disease_db']
collection = db['predictions']

def save_prediction(image_path, predicted_class, confidence):
    document = {
        "image_path": image_path,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(document)
