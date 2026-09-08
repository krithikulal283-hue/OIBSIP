def calculate_bmi(weight, height_cm):
    """
    Calculate BMI using weight in kilograms
    and height in centimeters.
    """

    height_m = height_cm / 100

    bmi = weight / (height_m ** 2)

    return bmi


def get_bmi_category(bmi):
    """
    Return BMI category based on BMI value.
    """

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


def validate_input(name, weight, height):
    """
    Validate user input.
    """

    # Check name
    if not name.strip():
        return False, "Please enter your name."

    # Check weight and height are numbers
    try:
        weight = float(weight)
        height = float(height)

    except ValueError:
        return False, "Weight and height must be numbers."

    # Check weight
    if weight <= 0:
        return False, "Weight must be greater than zero."

    # Check height
    if height <= 0:
        return False, "Height must be greater than zero."

    return True, ""