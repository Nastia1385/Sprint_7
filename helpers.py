import random
import string

import allure
from faker import Faker

fake = Faker()


def generate_unique_login():
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_string}"


def random_courier_data():
    return {
        "login": generate_unique_login(),
        "password": "TestPassword123",
        "firstName": "arti"
    }


def generate_order_data():
    """Метод для генерации тестовых данных заказа"""
    with allure.step("Генерация тестовых данных для заказа"):
        data = {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "address": fake.address(),
            "metroStation": 1,
            "phone": fake.phone_number(),
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": fake.text()
        }
        allure.attach(str(data), "Данные заказа", allure.attachment_type.JSON)
        return data
