import allure
import pytest

from conftest import random_courier_data
from data import BASE_URL
from scooter_api.courier_api import CourierAPI


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, random_courier_data):
        courier_api = CourierAPI(BASE_URL)
        # Отправить запрос на создание курьера
        response = courier_api.create_courier(
            random_courier_data["login"],
            random_courier_data["password"],
            random_courier_data["firstName"]
        )
        # Проверить код ответа"
        assert response.status_code == 201 and response.json() == {"ok": True}

        # Очистка: удаляем созданного курьера
        login_response = courier_api.login_courier(
            random_courier_data["login"],
            random_courier_data["password"]
        )
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            courier_api.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self):
        courier_api = CourierAPI(BASE_URL)
        test_login = "duplicate_test"
        test_password = "pass123"
        # Создаем курьера
        response1 = courier_api.create_courier(test_login, test_password, "Test")
        # Создаём повторно такого же курьера
        response2 = courier_api.create_courier(test_login, test_password, "Test2")
        assert response1.status_code == 201 and response2.status_code == 409

        # Очистка
        login_response = courier_api.login_courier(test_login, test_password)
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            courier_api.delete_courier(courier_id)

    @allure.title("Обязательные поля при создании курьера")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_missing_required_fields(self, missing_field):
        courier_api = CourierAPI(BASE_URL)
        # Создать курьера без поля {missing_field}
        if missing_field == "login":
            response = courier_api.create_courier("", "pass123", "Test")
        else:
            response = courier_api.create_courier("test_login", "", "Test")

        assert response.status_code == 400 and "Недостаточно данных" in response.json()["message"]

    @allure.title("Создание курьера без firstName успешно")
    def test_create_courier_without_firstname_success(self, random_courier_data):
        courier_api = CourierAPI(BASE_URL)
        # Создать курьера без firstName
        response = courier_api.create_courier(
            random_courier_data["login"],
            random_courier_data["password"]
        )
        assert response.status_code == 201 and response.json() == {"ok": True}

        # Очистка
        login_response = courier_api.login_courier(
            random_courier_data["login"],
            random_courier_data["password"]
        )
        if login_response.status_code == 200:
            courier_id = login_response.json().get("id")
            courier_api.delete_courier(courier_id)
