import pytest

from data import BASE_URL
from scooter_api.courier_api import CourierAPI


@pytest.fixture
def clean_courier(request):
    # Фикстура для создания и автоочистки курьера
    courier_api = CourierAPI(BASE_URL)
    created_couriers = []  # храним логины и пароли созданных курьеров

    def register_courier(login, password, first_name=None):
        #Вспомогательная функция для регистрации курьера в тесте
        response = courier_api.create_courier(login, password, first_name)
        if response.status_code == 201:
            created_couriers.append({"login": login, "password": password})
        return response

    # Возвращаем функцию регистрации и api клиент
    yield register_courier, courier_api

    # --- АВТООЧИСТКА (выполнится даже при падении теста) ---
    for courier in created_couriers:
        try:
            login_resp = courier_api.login_courier(courier["login"], courier["password"])
            if login_resp.status_code == 200:
                courier_id = login_resp.json().get("id")
                if courier_id:
                    courier_api.delete_courier(courier_id)
        except Exception as e:
            print(f"Ошибка при удалении {courier['login']}: {e}")


@pytest.fixture
def existing_courier():
    # Фикстура, создающая курьера для предусловия
    courier_api = CourierAPI(BASE_URL)
    login = "duplicate_test"
    password = "pass123"

    # Создаем курьера
    courier_api.create_courier(login, password, "Test")

    yield login, password, courier_api

    # Очистка после теста
    login_resp = courier_api.login_courier(login, password)
    if login_resp.status_code == 200:
        courier_id = login_resp.json().get("id")
        courier_api.delete_courier(courier_id)
