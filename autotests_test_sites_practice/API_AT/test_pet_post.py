import requests
import pytest



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