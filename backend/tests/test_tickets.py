import pytest

def test_health_and_readiness(client):
    assert client.get("/health").json()["status"] == "UP"
    assert client.get("/ready").json() == {"status": "READY"}

def test_create_and_read_ticket(client, ticket):
    response = client.post("/api/tickets", json=ticket)
    assert response.status_code == 201
    saved = response.json()
    assert saved["id"] > 0
    assert saved["status"] == "OPEN"
    assert saved["created_at"]
    assert client.get(f"/api/tickets/{saved['id']}").json() == saved

def test_list_filters_by_status(client, ticket):
    client.post("/api/tickets", json=ticket)
    client.post("/api/tickets", json={**ticket, "status": "RESOLVED"})
    assert len(client.get("/api/tickets").json()) == 2
    filtered = client.get("/api/tickets?status=RESOLVED").json()
    assert len(filtered) == 1 and filtered[0]["status"] == "RESOLVED"

def test_edit_changes_subject_status_and_priority(client, ticket):
    saved = client.post("/api/tickets", json=ticket).json()
    update = {**ticket, "subject": "VPN restored", "status": "RESOLVED", "priority": "LOW", "assignee": "Pranav"}
    response = client.put(f"/api/tickets/{saved['id']}", json=update)
    assert response.status_code == 200
    assert all(response.json()[key] == value for key, value in update.items())
    assert client.get(f"/api/tickets/{saved['id']}").json()["assignee"] == "Pranav"

def test_delete_removes_persisted_ticket(client, ticket):
    saved = client.post("/api/tickets", json=ticket).json()
    response = client.delete(f"/api/tickets/{saved['id']}")
    assert response.status_code == 204 and response.content == b""
    assert client.get(f"/api/tickets/{saved['id']}").status_code == 404
    assert client.get("/api/tickets").json() == []

@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_ticket_returns_404(client, ticket, method):
    kwargs = {"json": ticket} if method == "put" else {}
    assert getattr(client, method)("/api/tickets/999", **kwargs).status_code == 404

@pytest.mark.parametrize("field,value", [("subject", "   "), ("priority", "INVALID"), ("status", "CLOSED"), ("requester", ""), ("subject", "a" * 181)])
def test_invalid_input_does_not_persist(client, ticket, field, value):
    assert client.post("/api/tickets", json={**ticket, field: value}).status_code == 422
    assert client.get("/api/tickets").json() == []

def test_invalid_update_preserves_ticket(client, ticket):
    saved = client.post("/api/tickets", json=ticket).json()
    assert client.put(f"/api/tickets/{saved['id']}", json={**ticket, "status": None}).status_code == 422
    assert client.get(f"/api/tickets/{saved['id']}").json() == saved

def test_metrics_exposes_real_request_counter(client):
    client.get("/api/tickets")
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "text/plain" in metrics.headers["content-type"]
    assert 'relaydesk_http_requests_total{method="GET",route="/api/tickets",status="200"}' in metrics.text

def test_readiness_returns_503_on_database_failure(client):
    from sqlalchemy.exc import OperationalError
    from app.database import get_session
    from app.main import app
    class BrokenSession:
        def execute(self, statement):
            raise OperationalError("SELECT", {}, Exception("unavailable"))
    app.dependency_overrides[get_session] = lambda: BrokenSession()
    assert client.get("/ready").status_code == 503
    assert client.get("/health").status_code == 200
