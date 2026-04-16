import uuid

sessions = {}

def create_session(user):
    sid = str(uuid.uuid4())
    sessions[sid] = user
    return sid

def get_session(sid):
    return sessions.get(sid)

def delete_session(session_id):
    if session_id in sessions:
        del sessions[session_id]
        