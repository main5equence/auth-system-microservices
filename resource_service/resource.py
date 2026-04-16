from auth_service.token_service import verify_token
from auth_service.session_store import get_session
from rbac.roles import authorize
from rate_limit import is_allowed
from replay_detection import detect_replay


class ResourceService:

    # =========================
    # ADMIN RESOURCE (RBAC)
    # =========================
    def access_admin(self, token=None, session=None, mode="jwt"):

        if mode == "jwt":

            if not token:
                return "FAIL"

            data = verify_token(token)
            if not data:
                return "FAIL"

            # REPLAY ATTACK
            if detect_replay(token):
                return "REPLAY ATTACK DETECTED"

            user_id = data["user_id"]
            role = data["role"]

            # RATE LIMIT
            if not is_allowed(user_id):
                return "RATE LIMIT EXCEEDED"

            # RBAC
            if not authorize(role, "delete"):
                return "FORBIDDEN"

            return "ADMIN DATA"

        else:
            if not session:
                return "FAIL"

            user = get_session(session)
            if not user:
                return "FAIL"

            # RATE LIMIT
            if not is_allowed(user.username):
                return "RATE LIMIT EXCEEDED"

            # RBAC
            if not authorize(user.role, "delete"):
                return "FORBIDDEN"

            return "ADMIN DATA"

    # =========================
    # PROFILE (AUTHENTICATED)
    # =========================
    def get_profile(self, token=None, session=None, mode="jwt"):

        if mode == "jwt":
            if not token:
                return "FAIL"

            data = verify_token(token)
            
            if not data:
                return "FAIL"
            
            if detect_replay(token):
                return "REPLAY ATTACK DETECTED"

            return f"PROFILE DATA for {data['user_id']}"

        else:
            if not session:
                return "FAIL"

            user = get_session(session)
            if not user:
                return "FAIL"

            return f"PROFILE DATA for {user.username}"

    # =========================
    # USER DATA (RBAC read)
    # =========================
    def get_user_data(self, token=None, session=None, mode="jwt"):

        if mode == "jwt":
            if not token:
                return "FAIL"

            data = verify_token(token)
            if not data:
                return "FAIL"

            # REPLAY ATTACK
            if detect_replay(token):
                return "REPLAY ATTACK DETECTED"

            user_id = data["user_id"]
            role = data["role"]

            # RATE LIMIT
            if not is_allowed(user_id):
                return "RATE LIMIT EXCEEDED"

            # RBAC (read)
            if not authorize(role, "read"):
                return "FORBIDDEN"

            return "USER DATA"

        else:
            if not session:
                return "FAIL"

            user = get_session(session)
            if not user:
                return "FAIL"

            # RATE LIMIT
            if not is_allowed(user.username):
                return "RATE LIMIT EXCEEDED"

            if not authorize(user.role, "read"):
                return "FORBIDDEN"

            return "USER DATA"
        
