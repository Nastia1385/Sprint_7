import allure
import pytest

from data import BASE_URL
from scooter_api.courier_api import CourierAPI


class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    def test_login_courier_success(self, random_courier_data):
        courier_api = CourierAPI(BASE_URL)

        # Сначала создаем курьера
        courier_api.create_courier(
            random_courier_data["login"],
            random_courier_data["password"],
            random_courier_data["firstName"]
        )

        login_response = courier_api.login_courier(
            random_courier_data["login"],
            random_courier_data["password"]
        )

        assert login_response.status_code == 200 and "id" in login_response.json()

        # Очистка
        courier_id = login_response.json()["id"]
        courier_api.delete_courier(courier_id)

    @allure.title("Авторизация с неверным паролем")
    def test_login_wrong_password(self, random_courier_data):
        courier_api = CourierAPI(BASE_URL)

        # Создаем курьера
        courier_api.create_courier(
            random_courier_data["login"],
            random_courier_data["password"],
            random_courier_data["firstName"]
        )

        login_response = courier_api.login_courier(
            random_courier_data["login"],
            "wrong_password"
        )
        assert login_response.status_code == 404 and login_response.json()["message"] == "Учетная запись не найдена"

        # Очистка
        correct_login = courier_api.login_courier(
            random_courier_data["login"],
            random_courier_data["password"]
        )
        if correct_login.status_code == 200:
            courier_id = correct_login.json()["id"]
            courier_api.delete_courier(courier_id)

    @allure.title("Авторизация с несуществующим логином")
    def test_login_nonexistent_user(self):
        courier_api = CourierAPI(BASE_URL)

        login_response = courier_api.login_courier("nonexistent_user", "password123")

        assert login_response.status_code == 404 and login_response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_fields(self, missing_field):
        courier_api = CourierAPI(BASE_URL)

        if missing_field == "login":
            response = courier_api.login_courier("", "password123")
        else:
            response = courier_api.login_courier("test_login", "")

            # Проверить код ошибки и сообщение
        assert response.status_code == 400 and "Недостаточно данных" in response.json()["message"]
