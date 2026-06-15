import pytest

from data import BASE_URL
from scooter_api.courier_api import CourierAPI


@pytest.fixture
def create_courier_only(request):
    courier_api = CourierAPI(BASE_URL)
    created_couriers = []  # храним логины и пароли созданных курьеров

    def register_courier(login, password, first_name=None):
        response = courier_api.create_courier(login, password, first_name)
        if response.status_code == 201:
            created_couriers.append({"login": login, "password": password})
        return response

    # Сохраняем созданных курьеров в request для последующего удаления
    request.couriers_to_cleanup = created_couriers
    request.courier_api = courier_api

    return register_courier


@pytest.fixture
def cleanup_couriers(request):
    def cleanup():
        courier_api = getattr(request, 'courier_api', None)
        couriers = getattr(request, 'couriers_to_cleanup', [])

        if not courier_api:
            courier_api = CourierAPI(BASE_URL)

        for courier in couriers:
            try:
                login_resp = courier_api.login_courier(courier["login"], courier["password"])
                if login_resp.status_code == 200:
                    courier_id = login_resp.json().get("id")
                    if courier_id:
                        courier_api.delete_courier(courier_id)
            except Exception as e:
                print(f"Ошибка при удалении {courier['login']}: {e}")

    request.addfinalizer(cleanup)
