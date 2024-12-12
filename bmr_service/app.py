from flask import Flask, request, jsonify

app = Flask(__name__)

def bmr(weight, height, age, gender):
    """Calculates BMR"""
    result = 0
    if gender.lower() == "male":
        result = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender.lower() == "female":
        result = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        return None  # Invalid gender
    return result

@app.route('/bmr', methods=['GET'])
def calculate_bmr():
    """
    Calculates BMR based on weight, height, age, and gender
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)  # Run on port 5002
