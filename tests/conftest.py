import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from fast_zero.models import table_registry
from sqlalchemy.orm import Session
from src.fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    # gerenciamento de contexto
    with Session(engine) as session:
        yield session # esse é o objeto passado para o meu teste

    table_registry.metadata.drop_all(engine)
