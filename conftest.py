import pytest
from faker import Faker
import requests
from data import BASE_URL

fake = Faker()

# BASE_URL = "https://qa-scooter.education-services.ru"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def random_courier_data():
    """Генерация случайных данных для курьера"""
    return {
        "login": fake.user_name(),
        "password": fake.password(),
        "firstName": fake.first_name()
    }


@pytest.fixture
def created_courier_random(request, base_url):
    """Фикстура для создания и удаления курьера"""
    courier_data = {
        "login": fake.user_name(),
        "password": fake.password(),
        "firstName": fake.first_name()
    }

    # Создаем курьера
    response = requests.post(f"{base_url}/api/v1/courier", json=courier_data)

    # Логинимся чтобы получить ID
    login_response = requests.post(f"{base_url}/api/v1/courier/login",
                                   json={"login": courier_data["login"],
                                         "password": courier_data["password"]})
    courier_id = login_response.json().get("id")

    yield courier_data, courier_id

    # Удаляем курьера после теста
    if courier_id:
        requests.delete(f"{base_url}/api/v1/courier/{courier_id}")