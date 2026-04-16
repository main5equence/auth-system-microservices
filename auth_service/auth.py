from database.db import save_users, users_db
from user_service import user
from user_service.user import User
from auth_service.token_service import generate_refresh, generate_token
from auth_service.session_store import create_session
from auth_service.token_blacklist import add_to_blacklist
from auth_service.session_store import delete_session

import bcrypt
import qrcode
import pyotp

class AuthService:

    # =========================
    # REGISTER + QR (2FA)
    # =========================
    def register(self, username, password, role="user"):
        user = User(username, password, role)

        from database.db import save_users

        users_db[username] = {
            "password_hash": user.password_hash.decode(),
            "role": user.role,
            "totp_secret": user.totp_secret
        }

        save_users(users_db)

        # QR CODE GOOGLE AUTHENTICATOR
        totp = pyotp.TOTP(user.totp_secret)

        uri = totp.provisioning_uri(
            name=username,
            issuer_name="AuthSystem"
        )

        img = qrcode.make(uri)
        img.save(f"{username}_qr.png")

        print(f"[REGISTER] QR code saved as {username}_qr.png")

    # =========================
    # LOGIN
    # =========================
    def login(self, username, password):
        data = users_db.get(username)

        if not data:
            return None

        password_hash = data["password_hash"].encode()

        if bcrypt.checkpw(password.encode(), password_hash):
            user = User(username, password, data["role"])
            user.totp_secret = data["totp_secret"]
            return user

        return None
    


    # =========================
    # 2FA VERIFY
    # =========================
    def verify_2fa(self, user, code):
        return pyotp.TOTP(user.totp_secret).verify(code, valid_window=1)

    # =========================
    # TOKENS
    # =========================
    def issue_tokens(self, user):
        return {
            "jwt": generate_token(user.username, user.role),
            "refresh": generate_refresh(user.username, user.role),
            "session": create_session(user)
        }

    # =========================
    # LOGOUT (JWT blacklist)
    # =========================
    def logout(self, token):
        add_to_blacklist(token)

    def logout_session(self, session_id):
        delete_session(session_id)






