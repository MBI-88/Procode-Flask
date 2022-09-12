# Form ORM

# Packages
from wtforms import SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField

# Forms
class CommentUser(FlaskForm):
    """
    Formulario para aceptar los comentarios 

    Args:
        FlaskForm (object): Formulario de Flask
    """
    body = PageDownField(label='Danos tu opinion!',validators=[DataRequired(),
                                                    Length(2,100,message='Minimo 5 letras maximo 100')])
    submit = SubmitField(label='Send')


    
    