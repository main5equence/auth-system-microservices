used_tokens = set()

def detect_replay(token):
    if token in used_tokens:
        return True
    used_tokens.add(token)
    return False

def reset_replay():
    used_tokens.clear()