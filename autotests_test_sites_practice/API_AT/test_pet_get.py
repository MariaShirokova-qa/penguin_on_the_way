import requests
import pytest



def test_find_pets_by_status_available(petstore_auth_headers, petstore_base_url):
    """Получение списка питомцев в статусе "available" """

    params = {"status": "available"}

    # Передаём заголовки в GET-запрос
    response = requests.get(f"{petstore_base_url}/pet/findByStatus", params=params, headers=petstore_auth_headers)

    assert response.status_code == 200

    assert "application/json" in response.headers.get("content-type", "")

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        assert "name" in data[0]
        print(f"✅ Тест пройден! Нашли питомца: {data[0]['name']}")
        print(f"✅ Тест пройден! Количество доступных питомцев: {len(data)}")



def test_find_pets_by_status(petstore_auth_headers, petstore_base_url):
    """Получение списка питомцев в статусе "pending" """

    params = {"status": "pending"}

    response = requests.get(f"{petstore_base_url}/pet/findByStatus", params=params, headers=petstore_auth_headers)

    assert response.status_code == 200

    assert "application/json" in response.headers.get("content-type", "")

    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:
        assert "name" in data[0]

        print(f"✅ Тест пройден! Нашли питомца: {data[0]['name']}")
        print(f"✅ Тест пройден! Количество питомцев в ожидании: {len(data)}")




def test_find_pets_by_status_sold(petstore_auth_headers, petstore_base_url):
    """Получение списка питомцев в статусе "sold" """

    params = {"status": "sold"}

    response = requests.get(f"{petstore_base_url}/pet/findByStatus", params=params, headers=petstore_auth_headers)

    assert response.status_code == 200

    assert "application/json" in response.headers.get("content-type", "")

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        assert "name" in data[0]

        print(f"✅ Тест пройден! Нашли питомца: {data[0]['name']}")
        print(f"✅ Тест пройден! Количество проданных питомцев: {len(data)}")



def test_find_pets_by_status_all(petstore_auth_headers, petstore_base_url):
    """Получение списка питомцев во всех статусах """

    params = {"status": ["available", "pending", "sold"]}

    response = requests.get(f"{petstore_base_url}/pet/findByStatus", params=params, headers=petstore_auth_headers)

    assert response.status_code == 200

    assert "application/json" in response.headers.get("content-type", "")

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        assert "name" in data[0]

        print(f"✅ Тест пройден! Нашли питомца: {data[0]['name']}")
        print(f"✅ Тест пройден! Количество питомцев во всех статусах: {len(data)}")

    # Проверяем, что вернулись питомцы с нужными статусами
    # valid_statuses = ["available", "pending", "sold"]
    #for pet in
    #    assert pet["status"] in valid_statuses, f"Неожиданный статус: {pet['status']}"

    if data:
        print(f"🐾 Примеры: {[p['name'] for p in data[:3]]}")




@pytest.mark.parametrize("status", [
    "available",
    "pending",
    "sold"
])

def test_find_pets_by_single_status(petstore_auth_headers, petstore_base_url, status):
    """Один тест → три запуска с разными статусами"""

    params = {"status": status}

    response = requests.get(f"{petstore_base_url}/pet/findByStatus", params=params, headers=petstore_auth_headers)

    assert response.status_code == 200

    assert "application/json" in response.headers.get("content-type", "")

    data = response.json()
    assert isinstance(data, list)

    if len(data) > 0:
        assert "name" in data[0]

        print(f"✅ Тест пройден! Нашли питомца: {data[0]['name']}")
        print(f"✅ Тест пройден! Количество питомцев в статусе {status}: {len(data)}")



def test_create_pet_with_auth(petstore_auth_headers, petstore_base_url):
    """Создание питомца с авторизацией"""

    # Данные питомца
    new_pet = {
        "id": 12345,
        "name": "MyDog",
        "photoUrls": ["https://example.com/photo.jpg"],
        "status": "available"
    }

    # Отправляем POST с заголовками
    response = requests.post(f"{petstore_base_url}/pet", json=new_pet, headers=petstore_auth_headers)

    assert response.status_code in [200, 201]
    print("✅ Питомец создан!")
