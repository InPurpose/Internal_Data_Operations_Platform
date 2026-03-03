from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token(email, password):
    res = client.post(
        "/login",
        data={"username": email, "password": password}
    )
    return res.json()["access_token"]

def test_admin_access():
    token = get_token("admin@example.com", "password")
    response = client.get(
        "/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_user_cannot_access_admin():
    token = get_token("user0@example.com", "password")
    response = client.get(
        "/admin-only",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403