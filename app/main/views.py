# Views Main
# Packages
from flask import (render_template,redirect,
                   request,current_app,url_for,abort)
from flask_login import login_required,current_user
from flask_sqlalchemy import get_debug_queries
from .. import db
from app.models import Post, User
from . import main
from .forms import CommentUser


# Routes
# rutas principales de la aplicacion

@main.after_app_request
def after_request(response:str) -> object: # mide la latencia de la peticion a la base de datos (uso administrativo)
    """
    Mide la latencia de la peticion a la base de datos (uso administrativo)

    Args:
        response (str): respuesta recibida desde el navegador

    Returns:
        object: devuelve un objeto response
    """
    for query in get_debug_queries():
        if (query.duration >= current_app.config['FLASK_SLOW_DB_QUERY_TIME']):
            current_app.logger.warning(
                'Slow query: %s\nParamas: %s\nDurations: %f\nContext: %s\n' % \
                    (query.statement,query.parameters,query.duration,query.context))
    return response

# Ruta de inicio
@main.route('/') # Ruta de inicio
def index() -> render_template: 
    """
       Esta funcion es la encargada de generar la pagina de inicio 
    Returns:
        render_template: una plantilla html
    """
    return render_template('baseIndex.html')


@main.route('/post/',methods=['GET','POST'])
@login_required
def post() -> render_template: 
    """
    Puta que envia solo el post a la pagina de usuario 
    

    Returns:
        render_template: renderiza la web html
    """
    form = CommentUser()
    if form.validate_on_submit():
        comment = Post(body=form.body.data,
                       author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('.user',name=current_user._get_current_object().username))
    

@main.route('/user/<name>')
@login_required
def user(name:str) -> render_template: 
    """
    Ruta para el perfil de usario 

    Args:
        name (str): nombre del usuario

    Returns:
        render_template: renderiza la web html
    """
    usr = User.query.filter_by(username=name).first_or_404()
    page = request.args.get('page',1,type=int)
    pagination = usr.posts.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    url_next = pagination.next_num if pagination.has_next else None
    url_prev = pagination.prev_num if pagination.has_prev else None
    posts = pagination.items
    form = CommentUser()
    form.body.data = ''
    return render_template('user.html',usr=usr,
                           posts=posts,url_next=url_next,url_prev=url_prev,form=form)

@main.route('/shutdown')
def server_off() -> str: 
    """
    Apagado del servidor (solo es usada en el ambiente de testing)

    Returns:
        str: Mensaje de apagado
    """
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
    
    