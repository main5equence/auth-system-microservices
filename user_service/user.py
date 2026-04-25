import bcrypt
import pyotp

class User:
    def __init__(self, username, password, role, totp_secret=None):
        self.username = username
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.role = role

        if totp_secret:
            self.totp_secret = totp_secret
        else:
            self.totp_secret = pyotp.random_base32()
            
        
