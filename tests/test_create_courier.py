import allure
import pytest

from helpers import random_courier_data


class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, create_courier_only, cleanup_couriers):
        with allure.step("Создать курьера"):
            courier_data = random_courier_data()
            response = create_courier_only(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"]
            )

        assert response.status_code == 201 and response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self, create_courier_only, cleanup_couriers):
        courier_data = random_courier_data()

        with allure.step("Создать курьера"):
            response = create_courier_only(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"])

        with allure.step(f"Попробовать создать такого же курьера {courier_data["login"]} повторно"):
            response2 = create_courier_only(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"])

        assert response.status_code == 201 and response2.status_code == 409

    @allure.title("Создание курьера без firstName успешно")
    def test_create_courier_without_firstname_success(self, create_courier_only, cleanup_couriers):
        courier_data = random_courier_data()

        with allure.step(f"Создать курьера без firstName: {courier_data['login']}"):
            response = create_courier_only(
                courier_data["login"],
                courier_data["password"]
            )

        with allure.step("Проверить успешный ответ"):
            assert response.status_code == 201 and response.json() == {"ok": True}

    @allure.title("Обязательные поля при создании курьера")
    @pytest.mark.parametrize("login,password,expected_error", [
        ("", "pass123", "Недостаточно данных"),
        ("test_login", "", "Недостаточно данных"),
    ])
    def test_missing_required_fields(self, login, password, expected_error, create_courier_only, cleanup_couriers):
        with allure.step(f"Создать курьера с логином='{login}' и паролем='{password}'"):
            response = create_courier_only(login, password, "Test")

        with allure.step("Проверить, что вернулась ошибка 400 с соответствующим сообщением"):
            assert response.status_code == 400 and expected_error in response.json()["message"]
