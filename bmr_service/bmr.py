def bmr(weight, height, age, gender):
    """Calculates BMR given weight, height, age, and gender.

    Args:
        weight: Weight in kilograms (float).
        height: Height in centimeters (float).
        age: Age in years (int).
        gender: Gender ("male" or "female", string).

    Returns:
        The calculated BMR (float) or None if inputs are invalid.
    """
    if not (isinstance(weight, (int, float)) and isinstance(height, (int, float)) and isinstance(age, int)):
        raise TypeError("Weight and height must be numbers, and age must be an integer.")
    if not isinstance(gender, str):
        raise TypeError("Gender must be a string.")
    if weight <= 0 or height <= 0 or age <= 0:
        raise ValueError("Weight, height, and age must be positive values.")

    gender = gender.lower()
    if gender == "male":
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == "female":
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError('Invalid gender. Please specify "male" or "female".')
