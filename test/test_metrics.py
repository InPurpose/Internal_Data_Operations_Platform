from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_metrics_requires_auth():
    response = client.get("/metrics/gmv")
    assert response.status_code == 401