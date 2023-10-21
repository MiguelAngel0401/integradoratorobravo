from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, EmailField, 
                     SubmitField, ValidationError)
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

from models.users import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                    EqualTo('password_confirm', 
                                                            message='Las contraseñas deben coincidir')])
    password_confirm = PasswordField('Password Confirm', validators=[DataRequired()])
    submit = SubmitField('Registrar')

    ######## Validar Correo Unico #########
    def validate_email(self, field):
        ######## Consultar si el correo existe en la base de datos #######
        if User.check_email(field.data):
            raise ValidationError('El correo ya existe')

    ######## Validar Username Unico #########
    def validate_username(self, field):
        ######## Consultar si el username existe en la base de datos #######
        if User.check_username(field.data):
            raise ValidationError('El username ya existe')
        
        
################# Formulario de Login ##################
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

################ Formulario de Perfil ################
class ProfileForm(FlaskForm):
    # username No se edita
    # password No se edita
    # email, Verificar antes de actualizar
    first_name = StringField('Nombre',
                             validators=[DataRequired(), Length(min=3, max=30)])
    last_name = StringField('Apellidos', 
                            validators=[DataRequired(), Length(min=10, max=40)])
    image = FileField('Imagen de Perfil', 
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imagenes!')])
    submit = SubmitField('Actualizar')
    
class UpdateUserForm(FlaskForm):
    first_name = StringField('Nombre', validators=[DataRequired('Este campo es obligatorio')])
    last_name = StringField('Apellido', validators=[DataRequired('Este campo es obligatorio')])
    email = EmailField('Email', validators=[DataRequired(), Email('Usa una dirección de correo válida')])
    username = StringField('Usuario', validators=[DataRequired('Este campo es obligatorio')])