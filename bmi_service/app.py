from flask import Flask, request, jsonify

app = Flask(__name__)

def bmi(weight, height):
    """Calc BMI"""
    return weight / (height * height)

@app.route('/bmi', methods=['GET'])
def calculate_bmi():
    """
    Calculates BMI based on weight and height
    """
    weight = request.args.get('weight', type=float)
    height = request.args.get('height', type=float)

    if not weight or not height:
        return jsonify({'error': 'Weight and height are required parameters.'}), 400

    if weight <= 0 or height <= 0:
        return jsonify({'error': 'Weight and height must be positive values.'}), 400

    bmi_result = bmi(weight, height)
    return jsonify({'bmi': bmi_result})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
