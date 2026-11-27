"""Tests for the task management API."""

from unittest.mock import Mock

from fastapi.testclient import TestClient

import main


def test_root_and_addition() -> None:
    """Test the health endpoint and addition endpoint."""
    with TestClient(main.app) as client:
        root_response = client.get("/")
        addition_response = client.get("/addition", params={"a": 7, "b": 5})

    assert root_response.status_code == 200
    assert root_response.json() == {"message": "it works !"}
    assert addition_response.status_code == 200
    assert addition_response.json() == {"result a+b=": 12, "developer": "Dev1"}


def test_soustraction() -> None:
    """Test subtraction of two integers."""
    with TestClient(main.app) as client:
        response = client.get("/soustraction", params={"a": 5, "b": 3})

    assert response.status_code == 200
    assert response.json() == {"result a-b=": 2, "developer": "Dev1"}


def test_greeting(monkeypatch) -> None:
    """Test greeting data without depending on the host network."""
    monkeypatch.setattr(main.socket, "gethostname", lambda: "test-host")
    monkeypatch.setattr(main, "current_ip", lambda: "192.0.2.10")

    with TestClient(main.app) as client:
        response = client.get("/greeting", params={"name": "Alice"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, Alice",
        "developer": "Dev2",
        "hostname": "test-host",
        "IP": "192.0.2.10",
    }


def test_current_ip_success(monkeypatch) -> None:
    """Test the successful current IP lookup branch."""
    fake_socket = Mock()
    fake_socket.getsockname.return_value = ("192.0.2.20", 0)
    monkeypatch.setattr(main.socket, "socket", lambda *args: fake_socket)

    assert main.current_ip() == "192.0.2.20"
    fake_socket.close.assert_called_once()


def test_current_ip_fallback(monkeypatch) -> None:
    """Test the localhost fallback when the socket fails."""
    fake_socket = Mock()
    fake_socket.connect.side_effect = OSError
    monkeypatch.setattr(main.socket, "socket", lambda *args: fake_socket)

    assert main.current_ip() == "127.0.0.1"
    fake_socket.close.assert_called_once()


def test_multiply_and_divide() -> None:
    """Test multiplication, division, and division-by-zero handling."""
    with TestClient(main.app) as client:
        multiply_response = client.post("/multiply", json={"a": 2.5, "b": 4})
        divide_response = client.post("/divide", json={"a": 15, "b": 3})
        zero_response = client.post("/divide", json={"a": 15, "b": 0})

    assert multiply_response.status_code == 200
    assert multiply_response.json() == {"result a*b=": 10.0, "developer": "Dev1"}
    assert divide_response.status_code == 200
    assert divide_response.json() == {"result a/b=": 5.0, "developer": "Dev2"}
    assert zero_response.status_code == 400
    assert zero_response.json() == {"detail": "Division by zero"}


def test_items_and_remove() -> None:
    """Test listing, deleting, and rejecting a missing item."""
    original_item = main.items[3]
    try:
        with TestClient(main.app) as client:
            items_response = client.get("/items")
            remove_response = client.delete("/remove/3")
            missing_response = client.delete("/remove/3")

        assert items_response.status_code == 200
        assert [item["id"] for item in items_response.json()] == [1, 2, 3]
        assert remove_response.status_code == 200
        assert remove_response.json() == {"deleted": 3, "developer": "Dev1"}
        assert missing_response.status_code == 404
        assert missing_response.json() == {"detail": "Item not found"}
    finally:
        main.items[3] = original_item
