import json

FILE = "users.json"

# =========================
# LOAD FROM FILE
# =========================
def load_users():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# =========================
# SAVE TO FILE
# =========================
def save_users(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

# =========================
# GLOBAL "DATABASE"
# =========================
users_db = load_users()
