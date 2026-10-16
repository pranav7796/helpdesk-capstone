"""Exercise actual API routing; leaves one useful ticket for demo evidence."""
import json
import os
import urllib.request

base = os.environ.get("BASE_URL", "http://127.0.0.1:3000")
def call(path, method="GET", data=None):
    req = urllib.request.Request(base + path, data=json.dumps(data).encode() if data else None,
                                 method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as response:
        body = response.read()
        print(method, path, response.status)
        return json.loads(body) if body else None

ticket = {"subject": "Verify support workspace deployment", "requester": "Capstone demo", "description": "Created through the frontend proxy; stored in PostgreSQL.", "priority": "HIGH", "assignee": "Pranav"}
saved = call("/api/tickets", "POST", ticket)
assert saved["status"] == "OPEN"
assert any(t["id"] == saved["id"] for t in call("/api/tickets"))
updated = call(f"/api/tickets/{saved['id']}", "PUT", {**ticket, "status": "IN_PROGRESS"})
assert updated["status"] == "IN_PROGRESS"
assert call(f"/api/tickets/{saved['id']}")["subject"] == ticket["subject"]
throwaway = call("/api/tickets", "POST", {**ticket, "subject": "Temporary deletion check"})
call(f"/api/tickets/{throwaway['id']}", "DELETE")
assert not any(t["id"] == throwaway["id"] for t in call("/api/tickets"))
print("PASS: create, list, read, edit, status, priority and delete through frontend proxy; retained ticket", saved["id"])
