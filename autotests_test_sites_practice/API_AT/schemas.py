import pytest

@pytest.fixture
def schema_get_find_by_status():
    """Фикстура со схемой JSON для валидации ответа GET /pet/findByStatus"""
    return {
        "type": "object",
        "required": ["id", "status"],
        "properties": {
            "id": {"type": "integer"},
            "status": {"type": "string", "enum": ["available", "pending", "sold"]},
            "name": {"type": "string"},
            "photoUrls": {"type": "array", "items": {"type": "string"}}
        }
    }