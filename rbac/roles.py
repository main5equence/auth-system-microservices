roles_permissions = {
    "admin": ["read", "write", "delete"],
    "user": ["read"]
}

def authorize(role, action):
    return action in roles_permissions.get(role, [])
