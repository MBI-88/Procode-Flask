# Form ORM

# Packages
from ..exceptions import ValidationError
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Regexp
from flask_wtf import FlaskForm
from ..models import User

# Forms 
class RegisterUser(FlaskForm):
    """
    Formulario para registar a los usuarios nuevos

    Args:
        FlaskForm (object): Formulario de Flask
    """
    name = StringField(label='Name',validators=[DataRequired(),
                                                Length(4,10,message='Ponga su nombre solamente'),
                                                Regexp('^\w.*$',0,'El nombre puede tener letras,numeros ó puntos')])
    password = PasswordField(label='Password',validators=[DataRequired(),
                                                          Length(4,8,message='Debe tener minimo 8 caracteres')])
    password2 = PasswordField(label='Confirm password',validators=[DataRequired(),
                                                                   Length(4,8,message='Debe tener minimo 8 caracteres'),
                                                                   EqualTo('password',message='No coinciden los passwords')])
    submit = SubmitField(label='Register')
    
    def validate_name(self,field:str) -> ValueError:
        if (User.query.filter_by(username=field.data).first()):
            raise ValidationError('Username already in use')

class LoginUser(FlaskForm):
    """
    Formulario para realizar el login de antes de commentar

    Args:
        FlaskForm (object): Formulario de Flask
    """
    name = StringField(label='Username',validators=[DataRequired(),
                                                    Length(4,10,message='Ponga su nombre solamente'),
                                                    Regexp('^\w.*$',0,'El nombre puede tener letras,numeros ó puntos')]) 
    password = PasswordField(label='Password',validators=[DataRequired(),
                                                          Length(4,8,message='Debe tener minimo 4 caracteres')])
    remember_me = BooleanField('Remember')
    submit = SubmitField(label='Login')
    

