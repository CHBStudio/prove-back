import jwt
from datetime import datetime

from user.models import AuthToken

JWT_SECRET = 'PROKRUTYH'
JWT_ALGORITHM = 'HS256'


def generate_token(user_id, email, password):
    payload = {
        'email': email,
        'password': password
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM).decode('utf-8')
    try:
        user_token = AuthToken.objects.get(user_id=user_id)
        user_token.key = token
        user_token.save()
    except AuthToken.DoesNotExist:
        AuthToken(
            key=token,
            create_at=datetime.now(),
            user_id=user_id
        ).save()
    return token
