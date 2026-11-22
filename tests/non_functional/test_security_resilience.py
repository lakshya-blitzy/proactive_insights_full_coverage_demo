def test_security_headers_are_present(client):
    response = client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"

def test_unauthenticated_requests_are_rejected(client):
    assert client.get("/tasks").status_code == 401

def test_invalid_token_is_rejected(client):
    headers = {"Authorization": "Bearer invalid"}
    assert client.get("/tasks", headers=headers).status_code == 401

def test_health_response_time_sanity(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 1.0
