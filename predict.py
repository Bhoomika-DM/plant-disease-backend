import os
import json
import numpy as np
from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
from utils import preprocess_image
from config import MODEL_PATH, CLASS_NAMES_PATH
from database import save_prediction  # 🧠 Import MongoDB function

predict_route = Blueprint('predict_route', __name__)

# 🔁 Load model once
model = load_model(MODEL_PATH)

# 📄 Load class names
with open(CLASS_NAMES_PATH, 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# 📄 Load disease descriptions
with open('disease_info.json', 'r') as f:
    disease_info = json.load(f)

@predict_route.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    file.save(file_path)

    try:
        img_tensor = preprocess_image(file_path)
        predictions = model.predict(img_tensor)[0]
        predicted_idx = np.argmax(predictions)
        predicted_class = class_names[predicted_idx]
        confidence = float(predictions[predicted_idx]) * 100

        # 🧠 Get disease info
        info = disease_info.get(predicted_class, {})
        description = info.get('description', 'No description available.')
        care = info.get('care', 'No care tips available.')

        # ✅ Save to MongoDB
        save_prediction(
            image_path=file.filename,
            predicted_class=predicted_class,
            confidence=f"{confidence:.2f}%"
        )

        result = {
            'class': predicted_class,
            'confidence': f"{confidence:.2f}%",
            'description': description,
            'care': care
        }

        return jsonify(result)

    finally:
        os.remove(file_path)
