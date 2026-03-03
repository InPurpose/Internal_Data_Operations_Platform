from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post(
        "/login",
        data={"username": "user0@example.com", "password": "password"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_without_token():
    response = client.get("/protected")
    assert response.status_code == 401

def test_protected_with_token():
    login = client.post(
        "/login",
        data={"username": "user0@example.com", "password": "password"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200