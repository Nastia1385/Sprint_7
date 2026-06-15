from typing import Dict, Any

import allure

from data import BASE_URL
from scooter_api.order_api import OrderAPI


@allure.feature("Заказы")
@allure.story("Список заказов")
class TestOrdersList:

    def test_get_orders_list_returns_200(self):
        order_api = OrderAPI(BASE_URL)
        response = order_api.get_orders_list()
        assert response[0] == 200

    def test_get_orders_list_contains_orders_field(self):
        order_api = OrderAPI(BASE_URL)
        response = order_api.get_orders_list()
        data: Dict[str, Any] = response[1]

        assert "orders" in data, "В ответе отсутствует поле 'orders'"
        assert isinstance(data["orders"], list), "Поле 'orders' не является списком"

    def test_get_orders_list_order_structure(self):
        order_api = OrderAPI(BASE_URL)
        # получить список заказов
        list_response = order_api.get_orders_list()
        data = list_response[1]
        # проверить структуру любого (например, последнего) заказа
        orders = data["orders"]
        assert len(orders) > 0, "Нет заказов для проверки структуры"

        first_order = orders[0]
        expected_fields = ["id", "courierId", "firstName", "lastName", "address", "metroStation",
                           "phone", "rentTime", "deliveryDate", "track", "color", "comment",
                           "createdAt", "updatedAt", "status"]

        for field in expected_fields:
            assert field in first_order, f"Поле {field} отсутствует в ответе"
