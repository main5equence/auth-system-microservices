import jwt
import time
import secrets
import uuid

from auth_service.token_blacklist import is_blacklisted

# =========================
# SECRET KEY (JWT)
# =========================
SECRET = secrets.token_hex(32)

# =========================
# REFRESH TOKEN STORAGE
# =========================
refresh_tokens = {}

# =========================
# GENERATE REFRESH TOKEN
# =========================
def generate_refresh(user_id, role):
    token = str(uuid.uuid4())

    refresh_tokens[token] = (user_id, role)

    return token

# =========================
# REFRESH ACCESS TOKEN
# =========================
def refresh_access(refresh_token):
    data = refresh_tokens.get(refresh_token)

    if not data:
        return None

    user_id, role = data

    return generate_token(user_id, role)

# =========================
# GENERATE JWT
# =========================
def generate_token(user_id, role):
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": time.time() + 10  
    }

    return jwt.encode(payload, SECRET, algorithm="HS256")

# =========================
# VERIFY JWT
# =========================
def verify_token(token):

    if is_blacklisted(token):
        return None

    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    
