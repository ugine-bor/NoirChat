import os
from itsdangerous import URLSafeTimedSerializer


def generate_signed_token(app):
    random_bytes = os.urandom(16)
    token_str = random_bytes.hex()

    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(token_str)


def verify_token(token, app):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        token_str = serializer.loads(token, int(os.getenv('COOKIE_LIFE')))
        return bytes.fromhex(token_str)
    except:
        return None
