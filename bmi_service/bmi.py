def bmi(weight, height):
    """Calculates BMI given weight and height.

    Args:
        weight: Weight in kilograms (float).
        height: Height in meters (float).

    Returns:
        The calculated BMI (float) or None if inputs are invalid.
    """
    if not (isinstance(weight, (int, float)) and isinstance(height, (int, float))):
        raise TypeError("Weight and height must be numbers.")
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be positive values.")
    return weight / (height * height)
