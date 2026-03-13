import pytest

@pytest.fixture
def petstore_auth_headers():
    """Фикстура с заголовками для Petstore"""
    return {
        "api_key": "special-key",
        "Content-Type": "application/json"
    }

@pytest.fixture
def petstore_base_url():
    """Фикстура с заголовками для Petstore"""
    return "https://petstore.swagger.io/v2"