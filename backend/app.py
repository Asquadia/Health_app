from flask import Flask, request, jsonify, send_from_directory
from bmi import bmi
from bmr import bmr

app = Flask(__name__, static_folder='../frontend')

@app.route('/api/bmi', methods=['GET'])
def api_calculate_bmi():
    """
    endpoint to calculate BMI with the BMI service
    """
    weight = request.args.get('weight', type=float)
    height = request.args.get('height', type=float)

    if not weight or not height:
        return jsonify({'error': 'Weight and height are required parameters.'}), 400

    if weight <= 0 or height <= 0:
        return jsonify({'error': 'Weight and height must be positive values.'}), 400

    bmi_result = bmi(weight, height)
    return jsonify({'bmi': bmi_result})

@app.route('/api/bmr', methods=['GET'])
def api_calculate_bmr():
    """
    endpoint to calculate BMR, with the BMR service
    """
    weight = request.args.get('weight', type=float)
    height = request.args.get('height', type=float)
    age = request.args.get('age', type=int)
    gender = request.args.get('gender')

    if not weight or not height or not age or not gender:
        return jsonify({'error': 'Weight, height, age, and gender are required parameters.'}), 400
    
    if weight <= 0 or height <= 0 or age <= 0:
        return jsonify({'error': 'Weight, height, and age must be positive values.'}), 400

    bmr_result = bmr(weight, height, age, gender)
    if bmr_result is None:
        return jsonify({'error': 'Invalid gender. Please specify "male" or "female".'}), 400

    return jsonify({'bmr': bmr_result})

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run on port 5000
