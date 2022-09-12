# Main error handler
# Packages
from flask import render_template,request,jsonify
from . import main

# Routes
# routas para manipular los errores de la aplicacion

@main.app_errorhandler(403)
def forbidden(e:object) -> render_template:
    """

    Args:
        e (object): evento de error capturado

    Returns:
        render_template: _description_
    """
    if (request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html):
        response = jsonify({'error':'forbidden'})
        response.status_code = 403 
        return response
    return render_template('403.html'), 403

@main.app_errorhandler(404)
def page_not_found(e:object) -> render_template:
    """_summary_

    Args:
        e (object): evento de error capturado

    Returns:
        render_template: renderiza la web html
    """
    if (request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html):
        response = jsonify({'error':'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'),404

@main.app_errorhandler(500)
def internal_error(e:object) -> render_template:
    """_summary_

    Args:
        e (object): evento de error capturado

    Returns:
        render_template: renderiza la web html
    """
    if (request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html):
        response = jsonify({'error':'internal error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500
