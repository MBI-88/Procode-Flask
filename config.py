# Packages
import os,logging
from logging.handlers import SMTPHandler

# Base dir
basedir = os.path.abspath(os.path.dirname(__file__))

# Classes 
class Config():
    SECRET_KEY = os.environ.get('SECRECT_KEY') or os.urandom(20)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASK_MAIL_SUBJECT_PREFIX = '[ProC0d3]'
    FLASK_MAIL_SENDER = 'ProC0d3 <proc0d3@example.com>' 
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or 'Root'  # clave toor
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER','localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT','535'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','')
    FLASK_SLOW_DB_QUERY_TIME = 0.5
    SSL_REDIRECT = False
    FLASK_POSTS_PER_PAGE = 10

    
    @staticmethod
    def init_app(app:object) -> None:
        pass

# Development mode
class DevelopmentConfig(Config):
    DEBUG = True 
    MAIL_USE_TLS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir,'dev_db.sqlite')
    

# Test mode
class TestingConfig(Config):
    TESTING = True 
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir,'test_db.sqlite')
    WTF_CSRF_ENABLED = False

# Production mode
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRO_DATABASE_URI') or 'sqlite:///' + os.path.join(basedir,'prod_db.sqlite')
    
    @classmethod
    def init_app(cls:object,app:object) -> None:
        Config.init_app(app) 
        
        credentials = None 
        secure = None 
        if getattr(cls,'MAIL_USERNAME',None) is not None:
            credentials = (cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USE_TLS',None):
                secure = ()
        
        mail_handler = SMTPHandler(
        mailhost = (cls.MAIL_SERVER,cls.MAIL_PORT),
        fromaddr = cls.FLASK_MAIL_SENDER,
        toaddrs = [cls.FLASK_ADMIN_MAIL],
        subject = cls.FLASK_MAIL_SUBJECT_PREFIX + 'APPLICATION ERROR',
        credentials = credentials,
        secure = secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    

dictConfig = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    
}
    