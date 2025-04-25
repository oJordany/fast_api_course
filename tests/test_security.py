from jwt import decode

from fast_zero.security import create_access_token, settings


def test_jwt():
    data = {'sub': 'jordanyluiz@gmail.com'}
    token = create_access_token(data=data)

    result = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert result['sub'] == data['sub']
    assert result['exp']
