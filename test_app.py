import pytest
import json
from app import app  # Importing the Flask app from your main backend file

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_create_claim(client):
    response = client.post("/claim", json={
        "claim_id": "123",
        "policy_id": "POL123",
        "amount": 5000
    })
    assert response.status_code == 201 or response.status_code == 400  # Either created or duplicate claim ID
    

def test_get_claim(client):
    response = client.get("/claim/123")
    assert response.status_code in [200, 404]
    

def test_get_all_claims(client):
    response = client.get("/claim-list")
    assert response.status_code == 200
    assert isinstance(response.json["claims"], list)

def test_update_claim(client):
    response = client.put("/claim/123", json={"status": "Approved"})
    assert response.status_code in [200, 404]

def test_delete_claim(client):
    response = client.delete("/claim/123")
    assert response.status_code in [200, 404]

if __name__ == "__main__":
    pytest.main()