import pytest
from app.services import normalize_title, create_task, complete_task
from app.store import InMemoryStore

def test_normalize_title_collapses_whitespace():
    assert normalize_title("  prepare   release ") == "prepare release"

def test_create_task_rejects_blank_title():
    with pytest.raises(ValueError):
        create_task(InMemoryStore(), "  ", "alice")

def test_create_task_rejects_long_title():
    with pytest.raises(ValueError):
        create_task(InMemoryStore(), "x" * 121, "alice")

def test_non_owner_cannot_complete_task():
    store = InMemoryStore()
    task = store.create("review", "alice")
    with pytest.raises(PermissionError):
        complete_task(store, task["id"], "bob")
