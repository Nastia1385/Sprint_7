from typing import Dict, Any

import allure

from scooter_api.order_api import OrderAPI


@allure.feature("Заказы")
@allure.story("Список заказов")
class TestOrdersList:

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, base_url):
        order_api = OrderAPI(base_url)

        with allure.step("Отправить запрос на получение списка заказов"):
            response = order_api.get_orders_list()

        with allure.step("Проверить код ответа"):
            assert response[0] == 200

        with allure.step("Проверить, что тело ответа содержит список заказов"):
            data: Dict[str, Any] = response[1]
        assert "orders" in data, "В ответе отсутствует поле 'orders'" and isinstance(data["orders"], list)

        with allure.step("Проверить структуру первого заказа, если список не пуст"):
            orders = data["orders"]
        if len(orders) > 0:
            first_order = orders[0]
            expected_fields = ["id", "courierId", "firstName", "lastName", "address", "metroStation",
                               "phone", "rentTime", "deliveryDate", "track", "color", "comment",
                               "createdAt", "updatedAt", "status"]
            for field in expected_fields:
                assert field in first_order, f"Поле {field} отсутствует в ответе"
