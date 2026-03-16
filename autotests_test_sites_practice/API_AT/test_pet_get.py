import requests
import pytest
import jsonschema
from schemas import schema_get_find_by_status


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
    """Получение списка питомцев в статусе "sold", проверка валидации схемы вручную"""

    params = {"status": "sold"}

    response = requests.get(
        f"{petstore_base_url}/pet/findByStatus",
        params=params,
        headers=petstore_auth_headers
    )

    # HTTP-уровень
    assert response.status_code == 200, \
        f"Ожидали 200, получили {response.status_code}"

    assert "application/json" in response.headers.get("content-type", ""), \
        f"Ожидали application/json, получили {response.headers.get('content-type')}"

    # Структура данных
    data = response.json()
    assert isinstance(data, list), \
        f"Ожидали список, получили {type(data).__name__}"

    # Бизнес-логика
    if len(data) > 0:
        for pet in data:
            # Наличие обязательных полей
            assert "id" in pet, \
                f"У питомца нет id: {pet}"

            assert "status" in pet, \
                f"У питомца нет статуса: {pet}"

            # Типы данных обязательных полей
            assert isinstance(pet["id"], int), \
                f"id: ожидали int, получили {type(pet['id']).__name__}"

            assert isinstance(pet["status"], str), \
                f"status: ожидали str, получили {type(pet['status']).__name__}"

            # Типы данных опциональных полей
            if "name" in pet:
                assert isinstance(pet["name"], str), \
                    f"name: ожидали str, получили {type(pet['name']).__name__}"

            if "photoUrls" in pet:
                assert isinstance(pet["photoUrls"], list), \
                    f"photoUrls: ожидали list, получили {type(pet['photoUrls']).__name__}"

            # Значение соответствует запросу
            assert pet["status"] == "sold", \
                f"Питомец id={pet.get('id')}: ожидали 'sold', получили '{pet['status']}'"
    else:
        print("⚠️ Сервер вернул пустой список для статуса 'sold'")

    print(f"✅ Проверено {len(data)} питомцев со статусом 'sold'")



def test_find_pets_by_status_sold_auto_schema(petstore_auth_headers, petstore_base_url, schema_get_find_by_status, endpoint_get_find_by_status):
    """Получение списка питомцев в статусе "sold"
     проверка валидации схемы автоматически"""

    params = {"status": "sold"}

    response = requests.get(
        f"{petstore_base_url}{endpoint_get_find_by_status}",
        params = params,
        headers = petstore_auth_headers
    )

    # Базовые проверки
    assert response.status_code == 200

    data = response.json()

    # Валидация схемы
    jsonschema.validate(instance = data[0], schema = schema_get_find_by_status)



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



