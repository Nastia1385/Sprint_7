import requests

from data import BASE_URL, COURIERS_URL


class CourierAPI:
    # Класс для работы с API курьеров

    def __init__(self, base_url):
        self.created_courier_random = None
        self.base_url = base_url
        self.courier_url = f"{BASE_URL}{COURIERS_URL}"

    def create_courier(self, login, password, first_name=None):
        # Создание курьера
        data = {
            "login": login,
            "password": password
        }
        if first_name:
            data["firstName"] = first_name

        return requests.post(self.courier_url, json=data)

    def login_courier(self, login, password):
        # "Логин курьера"
        data = {
            "login": login,
            "password": password
        }
        return requests.post(f"{self.courier_url}/login", json=data)

    def delete_courier(self, courier_id):
        # Удаление курьера
        return requests.delete(f"{self.courier_url}/{courier_id}")
