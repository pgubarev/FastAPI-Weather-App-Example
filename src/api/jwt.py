import jwt

from conf import settings


def create_jwt(user):
    payload = {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'city_id': user.city_id,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def decode_jwt(token):
    try:
        return jwt.decode(token.credentials, settings.JWT_SECRET,
                          algorithms=["HS256"])
    except jwt.PyJWTError as ex:
        return None
