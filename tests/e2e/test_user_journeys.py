def test_complete_task_lifecycle(client):
    headers = {"Authorization": "Bearer demo-alice"}
    created = client.post("/tasks", json={"title": "Ship feature"}, headers=headers)
    assert created.status_code == 201
    task_id = created.json()["id"]
    assert any(t["id"] == task_id for t in client.get("/tasks", headers=headers).json())
    completed = client.post(f"/tasks/{task_id}/complete", headers=headers)
    assert completed.status_code == 200
    assert completed.json()["completed"] is True
    assert client.delete(f"/tasks/{task_id}", headers=headers).status_code == 204
