from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static')

# Get service URLs from environment variables or use defaults for local testing
BMI_SERVICE_URL = os.environ.get('BMI_SERVICE_URL', 'http://localhost:5001')
BMR_SERVICE_URL = os.environ.get('BMR_SERVICE_URL', 'http://localhost:5002')

@app.route('/api/bmi', methods=['GET'])
def api_calculate_bmi():
    """
    endpoint to calculate BMI with the BMI service
    """
    weight = request.args.get('weight')
    height = request.args.get('height')

    if not weight or not height:
        return jsonify({'error': 'Weight and height are required parameters.'}), 400

    try:
        response = requests.get(f'{BMI_SERVICE_URL}/bmi?weight={weight}&height={height}')
        response.raise_for_status()  # Raise an exception for bad status codes
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error contacting BMI service: {e}'}), 500

@app.route('/api/bmr', methods=['GET'])
def api_calculate_bmr():
    """
    endpoint to calculate BMR, with the BMR service
    """
    weight = request.args.get('weight')
    height = request.args.get('height')
    age = request.args.get('age')
    gender = request.args.get('gender')

    if not weight or not height or not age or not gender:
        return jsonify({'error': 'Weight, height, age, and gender are required parameters.'}), 400

    try:
        # Forward the request to the BMR service
        response = requests.get(f'{BMR_SERVICE_URL}/bmr?weight={weight}&height={height}&age={age}&gender={gender}')
        response.raise_for_status()

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error contacting BMR service: {e}'}), 500

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
