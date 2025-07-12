from flask import Flask, jsonify
from flask_cors import CORS
from predict import predict_route
app = Flask(__name__)
CORS(app)
app.register_blueprint(predict_route, url_prefix='/')
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Plant Disease Detection API is running!'})

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True)
