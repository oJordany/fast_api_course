import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from src.fast_zero.app import app


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    # gerenciamento de contexto
    with Session(engine) as session:
        yield session  # esse é o objeto passado para o meu teste

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(
        username='Teste',
        email='teste@teste.com',
        password='testtest',
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
