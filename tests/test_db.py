from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='jordany', email='mail@mail.com', password='1234')
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'mail@mail.com')
    )
    assert result.id == 1
    assert result.username == 'jordany'
