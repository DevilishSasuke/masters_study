import pytest
import asyncio
from fastapi.testclient import TestClient
from warehouse.main import app
from warehouse.db import init_db
import warehouse.models # noqa: F401

@pytest.fixture(autouse=True)
def prepare_database():
    # Запускаем твою асинхронную функцию создания таблиц
    asyncio.run(init_db())
    yield

client = TestClient(app)
TEST_ITEM_NAME = "test_item1"

def test_warehouse_logic():
    # проверка пустоты базы
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []

    # запрос к несуществующему предмету
    response = client.get(f"/items/{TEST_ITEM_NAME}")
    assert response.status_code == 404

    # помещение/создание предмета
    put_payload = {"amount": 50} 
    response = client.put(f"/items/{TEST_ITEM_NAME}", json=put_payload)
    
    assert response.status_code == 200
    assert response.json()["name"] == TEST_ITEM_NAME
    assert response.json()["amount"] == 50

    # создание заказа по предмету
    order_payload = {
        "name": TEST_ITEM_NAME
    }
    response = client.post("/orders", json=order_payload)

    # успешное создание
    assert response.status_code in (200, 201)
    order_data = response.json()

    # получаем айди для дальнейшего пользования
    created_order_id = order_data["id"]

    # получение заказа по айди
    response = client.get(f"/orders/{created_order_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == created_order_id
    assert response.json()["item_name"] == TEST_ITEM_NAME

    # удаление предмета
    response = client.delete(f"/items/{TEST_ITEM_NAME}")
    assert response.status_code == 204

    verify_response = client.get(f"/items/{TEST_ITEM_NAME}")
    assert verify_response.status_code == 404
