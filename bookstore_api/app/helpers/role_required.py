from functools import wraps
from flask_jwt_extended import get_current_user

from bookstore_api.app.helpers import handle_errors

def role_required(*required_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if get_current_user().role.name not in required_roles:
                return handle_errors('Unauthorized access', 403)
            return f(*args, **kwargs)
        return wrapper
    return decorator
