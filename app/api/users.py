# API para obtener todos los usuarios del sitio y sus posts
# Package
from flask import jsonify,current_app,request,url_for
from . import api
from ..models import User,Post,Permission
from .decorators import permission_required

# Api routes

@api.route('/users/')
@permission_required(Permission.ADMIN)
def get_all_users() -> dict: 
    """
    Devuelve todos los usuarios de la base de datos

    Returns:
        dict: devuelve un objeto jsonify interpretado por el navegador
    """
    user = User.query.all()
    userDic = {}
    for value in user:
        userDic[value.id] = {
            'name':value.username,
            'member_sice':value.member_since,
            'last_seen':value.last_seen
        }
    return jsonify(userDic)

@api.route('/posts/<int:id>')
@permission_required(Permission.ADMIN)
def get_posts(id:int) -> dict: 
    """
    Devuelve lso posts de un usuario en especifico pasando su identificador 

    Args:
        id (int): identificador de usuario

    Returns:
        dict: devuelve un objeto jsonify interpretado por el navegador
    """
    user = User.query.get_or_404(id)
    page = request.args.get('page',1,type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],error_out=False)
    
    posts = pagination.items
    url_prev = url_for('api.get_post',id=id,page=page - 1) if pagination.has_prev  else None
    url_next = url_for('api.get_post',id=id,page=page + 1) if pagination.has_next else None
    
    return jsonify({
        'username':user.username,
        'posts':[post.to_json() for post in posts],
        'next': url_next,
        'prev': url_prev,
        'count': pagination.total
    })



