# Decorator to verify permissions
# Packages
from functools import wraps
from flask_login import current_user
from flask import abort

# Decorator
def admin_required(permission:int) -> object:
    def decorator(f:object) -> object:
        @wraps(f)
        def decorated_function(*args, **kwargs) -> object:
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kwargs)
        return decorated_function
    return decorator

 

            
