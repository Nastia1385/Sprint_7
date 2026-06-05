from faker import Faker

fake = Faker()

import allure
import pytest

from data import BASE_URL
from scooter_api.order_api import OrderAPI


@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestCreateOrder:

    @pytest.fixture
    def order_data(self):
        """Фикстура с базовыми данными заказа"""
        return {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "address": fake.address(),
            "metroStation": 1,
            "phone": fake.phone_number(),
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": fake.text()
        }

    @allure.title("Создание нескольких заказов с параметризацией цветов")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_parametrized(self, base_url, order_data, colors):
        order_api = OrderAPI(BASE_URL)
        with allure.step(f"Создать заказ с цветами {colors}"):
            if colors:
                response = order_api.create_order(order_data, color=colors)
            else:
                response = order_api.create_order(order_data)
        assert response.status_code == 201 and "track" in response.json()
