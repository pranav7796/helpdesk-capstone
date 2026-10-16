import os

# Set before importing application code; tests never initialize the production DB.
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.database import Base, get_session
from app.main import app

@pytest.fixture
def client():
    engine = create_engine("sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    def test_session():
        with Session(engine) as session:
            yield session
    app.dependency_overrides[get_session] = test_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    engine.dispose()

@pytest.fixture
def ticket():
    return {"subject": "VPN connection fails", "description": "Cannot connect from home", "requester": "Asha", "priority": "HIGH"}
