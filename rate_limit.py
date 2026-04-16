import time

requests = {}

def is_allowed(user):
    now = time.time()

    if user not in requests:
        requests[user] = []

    # tylko ostatnie 10 sekund
    requests[user] = [t for t in requests[user] if now - t < 10]

    if len(requests[user]) > 5:
        return False

    requests[user].append(now)
    return True
