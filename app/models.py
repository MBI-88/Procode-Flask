# Packages 
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from markdown import markdown 
import bleach 
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app
from . import db,login_manager
import hashlib
import os
from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# Classes 
# Permission 
class Permission():
    """
    Clase que otroga los permisos al ususario actual
    """
    WRITE = 1
    READ = 2
    ADMIN = 4

class Role(db.Model):
    """
    Clase Role es usada para estableser los roles de cada usuario 
    en el sistema.
    Args:
        db (object): instancia de SQLARCHEMY para hacer encuestas a la base de datos

    Returns: None
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permisssion = db.Column(db.Integer)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __init__(self,**kwargs) -> None:
        super(Role,self).__init__(**kwargs)
        if self.permisssion is None:
            self.permisssion = 0
    
    @staticmethod
    def insert_roles() -> None:
        roles = {
            'User':[Permission.WRITE,Permission.READ],
            'Admin':[Permission.WRITE,Permission.READ,Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permissions(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        
        db.session.commit()
    
    def reset_permissions(self) -> None:
        self.permisssion = 0
    
    def add_permissions(self,perm:int) -> None:
        if not self.has_permissions(perm):
            self.permisssion += perm
    
    def has_permissions(self,perm:int) -> bool:
        return self.permisssion & perm == perm
    
    def __repr__(self) -> str:
        return '<Role %r>'% self.name
                
                
class User(UserMixin,db.Model):
    """
    Clase que administra los usuarios en la base de datos 
    Args:
        UserMixin (object): clase del modulo flask-login para los metodos de login
        db (object): instancia de SQLARCHEMY para hacer encuestas a la base de datos

    Raises:
        AttributeError: Lanza un error en caso de que se quiera acceder al password 

    Returns:
        _type_: None
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime(),default=datetime.utcnow())
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    
    
    def __init__(self,**kwargs) -> None:
        super(User,self).__init__( **kwargs)
        if self.role is None:
            if self.username == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        if self.username is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()
        
    
    @property
    def password(self) -> AttributeError:
        raise AttributeError('Password is not a readable attribute')
    
    
    @password.setter
    def password(self,password:str) -> None:
        self.password_hash = generate_password_hash(password)
    
    
    def verify_password(self,password:str) -> bool:
        return check_password_hash(self.password_hash,password)
    
    
    def can(self,perm:int) -> bool:
        return self.role is not None and self.role.has_permissions(perm)
    
    
    def gravatar(self,size=100,default='identicon',rating='g') -> str:
        url = "https://secure.gravatar.com/avatar"
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}%d={default}&r={rating}'.format(
            url=url,hash=hash,size=size,default=default,rating=rating)
    
    
    def gravatar_hash(self) -> str:
        return hashlib.md5(self.username.lower().encode('utf-8')).hexdigest()
    
    
    def __repr__(self) -> str:
        return '<User %r>'% self.username
    
    
    def is_admin(self) -> bool:
        return self.can(Permission.ADMIN)
    
    
    def ping(self) -> None:
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
    
    # Fake user (solo para desarrollo)
    @staticmethod
    def fake_users(count:int) -> None:
        fake = Faker()
        i = 0
        while i < count:
            usr = User(username=fake.user_name(),
                       password='password',
                       member_since=fake.past_date())
            
            db.session.add(usr)
            try: 
                db.session.commit()
                i += 1
            except IntegrityError :
                db.session.rollback()
    
    
    @staticmethod
    def verify_api_token(token:str) -> object:
        serial = Serializer(current_app.config['SECRET_KEY'],expires_in=3600)
        try:
            data = serial.loads(token)
        except: return None
        
        return User.query.get(data['id'])
    
    
    def generate_api_token(self) -> str:
        serial = Serializer(current_app.config['SECRET_KEY'],expires_in=3600)
        return serial.dumps({'id':self.id}).decode('utf-8')
    
    
    @staticmethod
    def csrf_token() -> str:
        serial = Serializer(current_app.config['SECRET_KEY'],expires_in=600)
        global salt
        salt = str(os.urandom(3))
        return serial.dumps({'csrf_token':salt}).decode('utf-8')
    
    
    @staticmethod
    def verify_csrf_token(token:str) -> bool:
        serial = Serializer(current_app.config['SECRET_KEY'],expires_in=600)
        try:
            csrf_token = serial.loads(token)
        except: return False
        
        if (salt == csrf_token['csrf_token']): return True
        
        
        
                
                
@login_manager.user_loader
def load_user(user_id:int) -> object:
    return User.query.get(int(user_id))


class Post(db.Model):
    """
    Clase que crea la tabla de Comentarios en la base
    de datos

    Args:
        db (object): instancia de SQLARCHEMY para hacer encuestas a la base de datos

    Raises:
        ValidationError: En caso de error pasa desapercibido

    Returns:
        _type_: None
    """
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    @staticmethod
    def on_change_body(target:object,value:str,oldvalue:str,initiator) -> None:
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value,output_format='html'),
            tags=allowed_tags,strip=True
        ))
        
    
    # Fakse post (solo para desarrollo)
    @staticmethod
    def fake_posts(count:int) -> None:
        fake = Faker()
        user_count = User.query.count()
        for i in range(count):
            usr = User.query.offset(randint(0,user_count - 1)).first()
            post = Post(body=fake.text(),
                        timestamp=fake.past_date(),
                        author=usr)
            
            db.session.add(post)
        db.session.commit()
    
    
    def to_json(self) -> dict:
        json_post = {
            'body': self.body,
            'body_html':self.body_html,
            'timestamp':self.timestamp,
        }
        return json_post
        
                
db.event.listen(Post.body,'set',Post.on_change_body)

class AnonimousUser(AnonymousUserMixin):
    """
    Clase que referencia al usuario no autenticado

    Args:
        AnonymousUserMixin (object): Clase base del modulo Flask-login
    """
    def can(self,permission:int) -> bool:
        return False
    
    def is_admin(self) -> bool:
        return False


login_manager.anonymous_user = AnonimousUser
    
    

