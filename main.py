from auth_service.auth import AuthService
from resource_service.resource import ResourceService
from replay_detection import reset_replay
from behavioral_auth.keystroke import KeystrokeAuth
from auth_service.token_blacklist import add_to_blacklist
from auth_service.token_service import refresh_access

import pyotp
import time

ks = KeystrokeAuth()
auth = AuthService()
res = ResourceService()

# =========================
# REGISTRATION (TYLKO RAZ!)
# =========================
print("\n=== REGISTRATION ===")
print("If first run → register users")
print("If already registered → skip (important for 2FA!)")

choice = input("Register users? (y/n): ")

if choice == "y":
    auth.register("admin", "pass", "admin")
    auth.register("user", "pass", "user")
    print("Scan QR codes NOW in Google Authenticator!")
    print("Then restart program and choose 'n'")
    exit()

# =========================
# LOGIN
# =========================
print("\n=== LOGIN ===")

username = input("Username (admin/user): ")
password = input("Password: ")

user = auth.login(username, password)

if not user:
    print("LOGIN FAIL")
    exit()

print(f"LOGIN OK as {user.role}")

# =========================
# KEYPSTROKE TRAINING
# =========================
print("\n=== KEYSTROKE TRAINING ===")
ks.train(username, "hello")

# =========================
# 2FA
# =========================
print("\n=== 2FA ===")
print("Open Google Authenticator and enter current code")

# DEBUG (możesz usunąć później)
print("DEBUG (should match your phone):",
      pyotp.TOTP(user.totp_secret).now())

code = input("Enter 2FA code: ")

if auth.verify_2fa(user, code):
    print("2FA OK")
else:
    print("2FA FAIL")
    print("Try again quickly or rescan QR")
    exit()

# =========================
# KEYPSTROKE VERIFY
# =========================
if ks.verify(username, "hello"):
    print("KEYSTROKE OK")
else:
    print("KEYSTROKE FAIL")
    exit()

# =========================
# TOKENS
# =========================
tokens = auth.issue_tokens(user)

jwt_token = tokens["jwt"]
session_id = tokens["session"]
refresh_token = tokens["refresh"]

# =========================
# VALID TOKEN
# =========================
print("\n=== VALID TOKEN ===")
reset_replay()
print(res.access_admin(token=jwt_token, mode="jwt"))

# =========================
# MISSING TOKEN
# =========================
print("\n=== MISSING TOKEN ===")
print(res.access_admin(token=None, mode="jwt"))

# =========================
# WRONG ROLE
# =========================
print("\n=== WRONG ROLE ===")

user2 = auth.login("user", "pass")

print("Enter code for USER account (Authenticator)")
code2 = input("2FA code: ")

if not auth.verify_2fa(user2, code2):
    print("2FA FAIL for user")
    exit()

tokens2 = auth.issue_tokens(user2)

print(res.access_admin(token=tokens2["jwt"], mode="jwt"))

# =========================
# TOKEN EXPIRATION
# =========================
print("\n=== TOKEN EXPIRATION ===")
reset_replay()

print("Waiting 11 seconds...")
time.sleep(11)

print(res.access_admin(token=jwt_token, mode="jwt"))

# =========================
# SESSION MODE
# =========================
print("\n=== SESSION MODE ===")
print(res.access_admin(session=session_id, mode="session"))

# =========================
# JWT vs SESSION
# =========================
print("\n=== JWT vs SESSION ===")
reset_replay()

print("JWT:", res.access_admin(token=jwt_token, mode="jwt"))
print("SESSION:", res.access_admin(session=session_id, mode="session"))

# =========================
# ROLE DEMO
# =========================
print("\n=== ROLE DEMO ===")

admin_user = auth.login("admin", "pass")

print("Enter code for ADMIN:")
admin_code = input("2FA code: ")

if not auth.verify_2fa(admin_user, admin_code):
    print("2FA FAIL")
    exit()

admin_tokens = auth.issue_tokens(admin_user)

print("Admin access:",
      res.access_admin(token=admin_tokens["jwt"], mode="jwt"))

print("User access:",
      res.access_admin(token=jwt_token, mode="jwt"))

# =========================
# LOGOUT TEST (JWT)
# =========================
print("\n=== LOGOUT TEST (JWT) ===")
add_to_blacklist(jwt_token)

print(res.access_admin(token=jwt_token, mode="jwt"))

# =========================
# SESSION LOGOUT TEST
# =========================
print("\n=== SESSION LOGOUT TEST ===")
auth.logout_session(session_id)

print(res.access_admin(session=session_id, mode="session"))

# =========================
# REFRESH TOKEN TEST
# =========================
print("\n=== REFRESH TOKEN TEST ===")

new_token = refresh_access(refresh_token)

print(res.access_admin(token=new_token, mode="jwt"))

# =========================
# REPLAY ATTACK TEST
# =========================
print("\n=== REPLAY ATTACK TEST ===")

reset_replay()

admin_user = auth.login("admin", "pass")

print("Enter code for ADMIN:")
admin_code = input("2FA code: ")

if not auth.verify_2fa(admin_user, admin_code):
    print("2FA FAIL")
    exit()

tokens_new = auth.issue_tokens(admin_user)
jwt_new = tokens_new["jwt"]

print("First request:",
      res.access_admin(token=jwt_new, mode="jwt"))

print("Second request:",
      res.access_admin(token=jwt_new, mode="jwt"))
