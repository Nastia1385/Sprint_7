import allure
import pytest

from data import BASE_URL
from helpers import random_courier_data
from scooter_api.courier_api import CourierAPI


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, clean_courier):
        register, courier_api = clean_courier

        with allure.step("Создать курьера"):
            courier_data = random_courier_data()
            response = register(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"]
            )

        assert response.status_code == 201 and response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self, existing_courier):
        login, password, courier_api = existing_courier

        with allure.step(f"Попробовать создать такого же курьера {login} повторно"):
            response2 = courier_api.create_courier(login, password, "Test2")

        assert response2.status_code == 409
        # первый курьер уже создан фикстурой, очистка авто

    @allure.title("Обязательные поля при создании курьера")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_missing_required_fields(self, missing_field, clean_courier):
        courier_api = CourierAPI(BASE_URL)

        with allure.step(f"Создать курьера без поля {missing_field}"):
            if missing_field == "login":
                response = courier_api.create_courier("", "pass123", "Test")
            else:
                response = courier_api.create_courier("test_login", "", "Test")

        with allure.step("Проверить, что вернулась ошибка 400 с соответствующим сообщением"):
            assert response.status_code == 400 and "Недостаточно данных" in response.json()["message"]

    @allure.title("Создание курьера без firstName успешно")
    def test_create_courier_without_firstname_success(self, clean_courier):
        courier_api = CourierAPI(BASE_URL)
        courier_data = random_courier_data()

        with allure.step(f"Создать курьера без firstName: {courier_data['login']}"):
            response = courier_api.create_courier(
                courier_data["login"],
                courier_data["password"]
            )

        with allure.step("Проверить успешный ответ"):
            assert response.status_code == 201 and response.json() == {"ok": True}

        
