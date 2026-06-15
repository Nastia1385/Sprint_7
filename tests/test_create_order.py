import allure
import pytest

from data import BASE_URL
from helpers import generate_order_data
from scooter_api.order_api import OrderAPI


@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание нескольких заказов с параметризацией цветов")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_parametrized(self, colors):
        order_api = OrderAPI(BASE_URL)
        order_data = generate_order_data()  # Вызываем метод из helpers

        with allure.step(f"Создать заказ с цветами {colors}"):
            response = order_api.create_order(order_data, color=colors)

        with allure.step("Проверить, что заказ успешно создан и получен track номер"):
            assert response.status_code == 201 and "track" in response.json()
