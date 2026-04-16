import bcrypt
import pyotp

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.role = role
        self.totp_secret = pyotp.random_base32()
        