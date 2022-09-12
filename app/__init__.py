# Packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import dictConfig
from flask_mail import Mail
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_moment import Moment

# Settings 
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login' # esta e la vista predeterminada para login
pagedown = PageDown()
moment = Moment()

# Factory

def create_app(envconfig:str) -> object:
    app = Flask(__name__)
    app.config.from_object(dictConfig[envconfig])
    dictConfig[envconfig].init_app(app)
    
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    moment.init_app(app)
    
    from .main import main as main_blu 
    app.register_blueprint(main_blu)
    
    from .auth import auth as auth_blu
    app.register_blueprint(auth_blu,url_prefix='/auth')

    from .api import api as api_blu 
    app.register_blueprint(api_blu,url_prefix='/api/v1')
    
    return app
    
    