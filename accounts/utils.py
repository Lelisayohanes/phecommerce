import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_verification_token(user):
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token valid for 1 day
    }, settings.SECRET_KEY, algorithm='HS256')
    return token