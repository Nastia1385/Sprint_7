import allure

from data import BASE_URL
from helpers import random_courier_data
from scooter_api.courier_api import CourierAPI


class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    def test_login_courier_success(self, existing_courier, clean_courier):
        login, password, courier_api = existing_courier
        courier_api = CourierAPI(BASE_URL)

        with allure.step(f"Авторизоваться с логином {login}"):
            login_response = courier_api.login_courier(
                login,
                password
            )

        with allure.step("Проверить успешную авторизацию и наличие id в ответе"):
            assert login_response.status_code == 200 and "id" in login_response.json()

    @allure.title("Авторизация с неверным паролем")
    def test_login_wrong_password(self, clean_courier):
        courier_api = CourierAPI(BASE_URL)
        courier_data = random_courier_data()

        with allure.step(f"Создать курьера с данными: {courier_data['login']}"):
            courier_api.create_courier(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"]
            )

        with allure.step(f"Попробовать авторизоваться с неверным паролем для {courier_data['login']}"):
            login_response = courier_api.login_courier(
                courier_data["login"],
                "wrong_password"
            )

        with allure.step("Проверить, что вернулась ошибка 404 с соответствующим сообщением"):
            assert login_response.status_code == 404 and login_response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация с несуществующим логином")
    def test_login_nonexistent_user(self, clean_courier):
        courier_api = CourierAPI(BASE_URL)

        with allure.step("Попробовать авторизоваться с несуществующим логином 'nonexistent_user'"):
            login_response = courier_api.login_courier("nonexistent_user", "password123")

        with allure.step("Проверить, что вернулась ошибка 404 с соответствующим сообщением"):
            assert login_response.status_code == 404 and login_response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация без логина")
    def test_login_missing_login(self, clean_courier):
        courier_api = CourierAPI(BASE_URL)

        with allure.step("Попробовать авторизоваться без логина"):
            response = courier_api.login_courier("", "password123")

        with allure.step("Проверить, что вернулась ошибка 400 с сообщением о недостаточности данных"):
            assert response.status_code == 400 and "Недостаточно данных" in response.json()["message"]

    @allure.title("Авторизация без пароля")
    def test_login_missing_password(self, clean_courier):
        courier_api = CourierAPI(BASE_URL)

        with allure.step("Попробовать авторизоваться без пароля"):
            response = courier_api.login_courier("test_login", "")

        with allure.step("Проверить, что вернулась ошибка 400 с сообщением о недостаточности данных"):
            assert response.status_code == 400 and "Недостаточно данных" in response.json()["message"]
