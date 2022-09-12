# Views of auth
# Packages
from flask import render_template,redirect,request,url_for,flash,current_app
from . import auth
from ..models import Post,User,Permission
from .. import db
from flask_login import current_user,login_required,login_user,logout_user
from .forms import LoginUser,RegisterUser
from ..decorators import admin_required


# Middelware de confirmacion de usuario autenticado
@auth.before_app_request
def before_request() -> None: 
    """
    Middelware de confirmacion de usuario autenticado
    """
    if current_user.is_authenticated:
        current_user.ping() 


# Routes

@auth.route('/login',methods=['GET','POST'])
def login() -> render_template: # ruta para logear a un usuarios registrado
    """
    Ruta para logear a un usuarios registrado

    Returns:
        render_template: renderiza la web html
    """
    form = LoginUser()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            if not current_user.is_admin(): # si no es admin se redirige a la pagina de ususrio normal
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.user',name=user.username)
                return redirect(next)
            
            return redirect(url_for('.profileAdmin')) # si es admin se redirige a la pagina del profileAdmin
    
        flash('Invalid name or password !',category='error')
    return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required
def logout() -> render_template: # cerrar sesion en el sistema
    """
    Cerrar sesion en el sistema

    Returns:
        render_template: renderiza la web html
    """
    logout_user()
    flash("You've been logged out!")
    return render_template('auth/logout.html')


@auth.route('/register',methods=['GET','POST'])
def register() -> render_template: 
    """
    Registrar usuario en el sistema

    Returns:
        render_template: renderiza la web html
    """
    form = RegisterUser()
    if form.validate_on_submit():
        user = User(
            username=form.name.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Registration successfull!')
        return redirect(url_for('main.user',name=user.username))

    return render_template('auth/register.html',form=form)


@auth.route('/admin')
@admin_required(Permission.ADMIN)
def profileAdmin() -> render_template: 
    """
    Ruta solo para administradores 

    Returns:
        render_template: renderiza la web html
    """
    page = request.args.get('page',1,type=int)
    name = current_user.username
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=current_app.config['FLASK_POSTS_PER_PAGE'],
        error_out=False)
    url_next = pagination.next_num if pagination.has_next else None
    url_prev = pagination.prev_num if pagination.has_prev else None
    posts = pagination.items
    return render_template('auth/profileAdmin.html',name=name,
                           posts=posts,url_next=url_next,url_prev=url_prev)