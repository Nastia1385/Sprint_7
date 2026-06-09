import random
import string


def generate_unique_login():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_string}"


def random_courier_data():
    return {
        "login": generate_unique_login(),
        "password": "TestPassword123",
        "firstName": "arti"
    }
