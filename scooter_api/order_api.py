import requests

from data import BASE_URL, ORDERS_URL


class OrderAPI:
    # Класс для работы с API заказов

    def __init__(self, base_url):
        self.base_url = base_url
        self.order_url = f"{BASE_URL}{ORDERS_URL}"

    def create_order(self, data, color=None):
        order = data.copy()

        if color:
            order["color"] = color

        return requests.post(self.order_url, json=order)

    # Получение списка заказов"""
    def get_orders_list(self):
        response = requests.get(f'{BASE_URL}{ORDERS_URL}')
        return response.status_code, response.json()

    def get_order(self, id):
        response = requests.get(f'{BASE_URL}{ORDERS_URL}/{id}')
        return response, None

    def delete_order(self, id, params):
        response = requests.delete(f'{BASE_URL}{ORDERS_URL}/{id}', data=params)
        return response.status_code, response
