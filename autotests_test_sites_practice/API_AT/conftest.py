import pytest

@pytest.fixture
def petstore_auth_headers():
    """Фикстура с заголовком для авторизации"""
    return {
        "api_key": "special-key",
        "Content-Type": "application/json"
    }

@pytest.fixture
def petstore_base_url():
    """Фикстура с заголовком урла"""
    return "https://petstore.swagger.io/v2"


@pytest.fixture
def endpoint_get_find_by_status():
    """Фикстура с ручкой /pet/findByStatus"""
    return "/pet/findByStatus"