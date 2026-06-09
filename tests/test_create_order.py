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
        # Фикстура с базовыми данными заказа
        with allure.step("Генерация тестовых данных для заказа"):
            data = {
                "firstName": fake.first_name(),
                "lastName": fake.last_name(),
                "address": fake.address(),
                "metroStation": 1,
                "phone": fake.phone_number(),
                "rentTime": 5,
                "deliveryDate": "2024-12-31",
                "comment": fake.text()
            }
            allure.attach(str(data), "Данные заказа", allure.attachment_type.JSON)
            return data

    @allure.title("Создание нескольких заказов с параметризацией цветов")
    @pytest.mark.parametrize("colors", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        None
    ])
    def test_create_order_parametrized(self, order_data, colors):
        order_api = OrderAPI(BASE_URL)

        with allure.step(f"Создать заказ с цветами {colors}"):
            if colors:
                response = order_api.create_order(order_data, color=colors)
            else:
                response = order_api.create_order(order_data)

        with allure.step("Проверить, что заказ успешно создан и получен track номер"):
            assert response.status_code == 201 and "track" in response.json()
