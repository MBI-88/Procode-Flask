# API decorator
# Packages
from functools import wraps
from flask import g
from .errors import forbidden

# Decorator

def permission_required(permission:int) -> object: 
    """
    Decorador usado para verificar si es administrador en el script authentication

    Args:
        permission (int): permisos dado por el sistema al usuario

    Returns:
        object: funcion devuelta por el decorador
    """
    def decorator(f:object) -> object:
        @wraps(f)
        def decorated_func(*args,**kwargs) -> object:
            if not g.current_user.can(permission):
                return forbidden("You don't haver permission!")
            return f(*args,**kwargs)
        return decorated_func
    return decorator