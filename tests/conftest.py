import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.store import store

@pytest.fixture
def client():
    store.tasks.clear()
    store.next_id = 1
    return TestClient(app)
