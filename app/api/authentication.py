# API login 
# Packages
from sympy import per
from .decorators import permission_required
from . import api
from .errors import unauthrized,forbidden
from flask_httpauth import HTTPBasicAuth
from ..models import User,Permission
from flask import jsonify,g,request
from .. import db

auth = HTTPBasicAuth()

# API routes

@auth.verify_password
def verify_password(name_or_token:str,password:str) -> bool: 
    """
    Middleware, capa intermedia para verificar credenciales

    Args:
        name_or_token (str): nombre de usurio o token recibido para credenciales
        password (str): clave del usuario en el sistema

    Returns:
        bool: verdadero o falso (en caso de falso se captura como error)
    """
    if (name_or_token == ''): return False
    
    if (password == ''):
        g.current_user = User.verify_api_token(name_or_token)
        g.token_used = True
        return g.current_user is not None

    user = User.query.filter_by(username=name_or_token).first()
    
    if (not user):
        return False
    
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error() -> dict: # captura los errores dando como salida codigos de html (400,401,500)
    """
    Captura los errores dando como salida codigos de html (400,401,500)

    Returns:
        dict: objeto tipo diccionario 
    """
    return unauthrized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request() -> dict: 
    """
    Impide el paso del usuario si no es admin

    Returns:
        dict: objeto tipo diccionario
    """
    if  g.current_user.is_anonymous:
        return forbidden('Access denied')



@api.route('/token/')
@permission_required(Permission.ADMIN)
def get_token() -> dict: 
    """
    Eniva un token para no tener que usar credenciales (mas seguridad)

    Returns:
        dict: objeto tipo diccionario
    """
    if g.current_user.is_anonymous or g.token_used:
        return unauthrized('Invalid credentials!')
    return jsonify({'token':g.current_user.generate_api_token(),'expiration_(s)':3600})



@api.route('/register/', methods=['GET'])
@permission_required(Permission.ADMIN) # si no es admin no tiene acceso
def registerGet() -> dict: 
    """
    Envia el formulario (solo puede ser usado por el administrador)

    Returns:
        dict: objeto tipo diccionario
    """
    csrf_token = User.csrf_token()
    
    # el formulario de regreso debe terner los mimos valores que son dados a partir de la clave
    # ejemplo <input name="name">,<input name="csrf_token">,etc
    
    form = {
        'csrf_token': csrf_token,
        'username': 'name',
        'password': 'password',
        'password2': 'password'
    }
    return jsonify(form)


@api.route('/register/', methods=['POST'])
@permission_required(Permission.ADMIN) # si no es admin no tiene acceso
def registerPost() -> dict: 
    """
    Recibe el formulario

    Returns:
        dict: objeto tipo diccionario
    """
    csrf_token = request.form.get('csrf_token')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    
    if (User.verify_csrf_token(csrf_token) and password == password2):
        usr = User(username=name,password=password)
        db.session.add(usr)
        db.session.commit()
        return jsonify({
            'done':'Successfull!'
        })
    
    return jsonify({
        'error': 'Token expired!'
    })
        
        
    
    
    
    
    


    


