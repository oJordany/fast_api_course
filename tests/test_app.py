from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (ação)
    assert response.status_code == HTTPStatus.OK  # Assert (afirmando)
    assert response.json() == {'message': 'Hello World'}  # Assert (afirmando)


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testeusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    # voltou o status code correto ?
    assert response.status_code == HTTPStatus.CREATED
    # validar UserPublic
    assert response.json() == {
        'username': 'testeusername',
        'id': 1,
        'email': 'test@test.com',
    }


# Não é uma prática boa um teste depender da exec de outro anterior
def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    # o user que recebemos é do sqlAlchemy, convertemos para Pydantic model
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [user_schema],
    }


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'teste',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    assert response.json() == {
        'username': 'teste',
        'id': 1,
        'email': 'test@test.com',
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'teste',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_read_user_by_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_user_by_id_not_found(client):
    response = client.get('/user/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_create_user_with_same_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    # voltou o status code correto ?
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # validar UserPublic
    assert response.json() == {'detail': 'Username already registered'}


def test_create_user_with_same_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste2',
            'password': 'password',
            'email': 'teste@teste.com',
        },
    )
    # voltou o status code correto ?
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # validar UserPublic
    assert response.json() == {'detail': 'Email already registered'}
