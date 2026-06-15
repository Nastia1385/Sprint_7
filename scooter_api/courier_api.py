import allure
import requests

from data import BASE_URL, COURIERS_URL


class CourierAPI:
    def __init__(self, base_url):
        self.base_url = base_url
        self.courier_url = f"{BASE_URL}{COURIERS_URL}"

    @allure.step("Создание курьера с логином '{login}'")
    def create_courier(self, login, password, first_name=None):
        data = {
            "login": login,
            "password": password
        }
        if first_name:
            data["firstName"] = first_name
        return requests.post(f"{BASE_URL}{COURIERS_URL}", json=data)

    @allure.step("Логин курьера с логином '{login}'")
    def login_courier(self, login, password):
        data = {
            "login": login,
            "password": password
        }
        return requests.post(f"{BASE_URL}{COURIERS_URL}/login", json=data)

    @allure.step("Удаление курьера с id '{courier_id}'")
    def delete_courier(self, courier_id):
        return requests.delete(f"{BASE_URL}{COURIERS_URL}/{courier_id}")
