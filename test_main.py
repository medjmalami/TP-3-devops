from fastapi.testclient import TestClient

from main import app


def test_soustraction() -> None:
    with TestClient(app) as client:
        response = client.get("/soustraction", params={"a": 5, "b": 3})

    assert response.status_code == 200
    assert response.json() == {"result a-b=": 2, "developer": "Dev1"}
