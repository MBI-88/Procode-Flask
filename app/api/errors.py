# API errors
# Packages
from flask import jsonify
from ..exceptions import ValidationError
from . import api

# Functions
# funciones de ayuda para la captura de errores en authentication.py 

def bad_request(message:str) -> dict:
    """
    Funciones de ayuda para la captura de errores en authentication.py 

    Args:
        message (str): mensaje hacia el cliente

    Returns:
        dict: objeto tipo diccionario
    """
    response = jsonify({'error':'bad request','message':message})
    response.status_code = 400
    return response

def unauthrized(message:str) -> dict:
    """
    Funciones de ayuda para la captura de errores en authentication.py 

    Args:
        message (str): mensaje hacia el cliente

    Returns:
        dict: objeto tipo diccionario
    """
    response = jsonify({'error':'unauthorized','message':message})
    response.status_code = 401
    return response

def forbidden(message:str) -> dict:
    """
    Funciones de ayuda para la captura de errores en authentication.py 

    Args:
        message (str): mensaje hacia el cliente

    Returns:
        dict: objeto tipo diccionario
    """
    response = jsonify({'error':'forbidden','message':message})
    response.status_code = 403
    return response



@api.errorhandler(ValidationError)
def validation_error(e:object) -> ValidationError:
    """
    Validador de error de la api

    Args:
        e (object): mensaje hacia el cliente

    Returns:
        ValidationError: clase para capturar errores
    """
    return bad_request(e.args[0])