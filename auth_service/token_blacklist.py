blacklist = set()

def add_to_blacklist(token):
    blacklist.add(token)

def is_blacklisted(token):
    return token in blacklist
