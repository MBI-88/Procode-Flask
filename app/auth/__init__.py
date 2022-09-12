# athu Blueprint
# Packages
from flask import Blueprint

# config
auth = Blueprint('auth',__name__)

from .import views

