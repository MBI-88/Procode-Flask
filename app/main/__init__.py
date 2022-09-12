# Blueprint

# Packages
from flask import Blueprint

# Main 
main = Blueprint('main',__name__)
from . import views,errors
from ..models import Permission

@main.app_context_processor
def inject_permission() -> dict: # Permite el acceso de los permisos en las plantillas
    return dict(Permission = Permission)