import secrets
import string


def generate_password(length, use_uppercase, use_lowercase,
                      use_numbers, use_special):

    characters = ""

    if use_uppercase:
        characters += string.ascii_uppercase

    if use_lowercase:
        characters += string.ascii_lowercase

    if use_numbers:
        characters += string.digits

    if use_special:
        characters += string.punctuation

    if not characters:
        raise ValueError(
            "Please select at least one character type."
        )

    if length < 4:
        raise ValueError(
            "Password length must be at least 4 characters."
        )

    password = "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

    return password


def calculate_strength(password):

    score = 0

    # Length
    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if len(password) >= 16:
        score += 1

    # Lowercase
    if any(char.islower() for char in password):
        score += 1

    # Uppercase
    if any(char.isupper() for char in password):
        score += 1

    # Numbers
    if any(char.isdigit() for char in password):
        score += 1

    # Special characters
    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 2:
        return "Weak"

    elif score <= 4:
        return "Medium"

    elif score <= 6:
        return "Strong"

    else:
        return "Very Strong"
    