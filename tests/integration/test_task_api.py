def auth(user="alice"):
    return {"Authorization": f"Bearer demo-{user}"}

def test_create_and_list_tasks(client):
    response = client.post("/tasks", json={"title": "Review PR"}, headers=auth())
    assert response.status_code == 201
    assert response.json()["title"] == "Review PR"
    assert len(client.get("/tasks", headers=auth()).json()) == 1

def test_user_cannot_complete_another_users_task(client):
    task = client.post("/tasks", json={"title": "Private"}, headers=auth()).json()
    response = client.post(f"/tasks/{task['id']}/complete", headers=auth("bob"))
    assert response.status_code == 403

def test_delete_removes_task(client):
    task = client.post("/tasks", json={"title": "Temporary"}, headers=auth()).json()
    response = client.delete(f"/tasks/{task['id']}", headers=auth())
    assert response.status_code == 204
    assert client.get("/tasks", headers=auth()).json() == []
