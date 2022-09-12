# Script to send email confirmation account
# Packages
from threading import Thread
from flask import current_app,render_template
from flask_mail import Message
from . import mail

# Functions
def send_async_email(app:object,msg:str) -> None:
    with app.app_context():
        mail.send(msg)

def send_email(to:str,subject:str,template:str,**kwargs) -> Thread:
    app = current_app._get_current_object()
    msg = Message(
        app.config['FLASK_MAIL_SUBJECT_PREFIX']+ ' '+ subject,
        sender=app.config['FLASK_MAIL_SENDER'],recipients=[to]
    )
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    
    thred = Thread(target=send_async_email,args=[app,msg])
    thred.start()
    return thred