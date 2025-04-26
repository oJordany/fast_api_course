from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='jordany', email='mail@mail.com', password='1234')
    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'mail@mail.com'))
    assert result.id == 1
    assert result.username == 'jordany'


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        json={
            'title': 'Test todo',
            'description': 'Test description',
            'state': 'draft',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_data = {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test description',
        'state': 'draft',
    }

    data = response.json()

    for key, value in expected_data.items():
        assert data[key] == value

    assert 'created_at' in data
    assert 'updated_at' in data
