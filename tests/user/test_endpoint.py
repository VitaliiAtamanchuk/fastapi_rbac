from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_user(client: TestClient) -> None:
    response = client.post("/users/create")
    assert response.status_code == 403
