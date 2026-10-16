import time
from fastapi import Depends, FastAPI, HTTPException, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from .api import router
from .database import get_session

app = FastAPI(title="Relaydesk Support API", version="1.0.0")
app.include_router(router)
requests = Counter("relaydesk_http_requests_total", "Completed HTTP requests", ["method", "route", "status"])
latency = Histogram("relaydesk_http_request_duration_seconds", "HTTP response time", ["method", "route"])

@app.middleware("http")
async def observe_requests(request, call_next):
    started = time.perf_counter()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        route = getattr(request.scope.get("route"), "path", "unmatched")
        if route != "/metrics":
            requests.labels(request.method, route, str(status)).inc()
            latency.labels(request.method, route).observe(time.perf_counter() - started)

@app.get("/health", tags=["operations"])
def health():
    return {"status": "UP", "service": "relaydesk"}

@app.get("/ready", tags=["operations"])
def ready(session: Session = Depends(get_session)):
    try:
        # Readiness also checks migration availability, not just a TCP connection.
        session.execute(text("SELECT id FROM tickets LIMIT 1"))
    except SQLAlchemyError:
        raise HTTPException(503, "Database unavailable or migrations pending") from None
    return {"status": "READY"}

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), headers={"Content-Type": CONTENT_TYPE_LATEST})
