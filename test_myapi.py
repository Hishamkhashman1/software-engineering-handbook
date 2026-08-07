from fastapi.testclient import TestClient
from myapi import app

client = TestClient(app)

def test_route():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "it works, I think"}
