from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField
from wtforms.fields import EmailField, TextAreaField, PasswordField, RadioField
from wtforms import validators

def mi_validacion(form,field):
    if len(field.data)==0:
        raise validators.ValidationError('El campo no tiene datos')


class UserForm(Form):
    matricula = StringField('Matricula',
    [validators.DataRequired('El Campo Matricula es requerido'),
     validators.length(min=5,max=10,message='Ingresa min 5 max 10')])
    nombre = StringField('Nombre',
     [validators.DataRequired('El Campo Nombre es requerido')])
    apaterno = StringField('Apaterno',[
        mi_validacion])
    amaterno = StringField('Amaterno')
    email = EmailField('Correo')

class Palabra(Form):
    # Palabra para el traductor
    palabra = StringField('Ingresa la palabra a traducir',
    [mi_validacion])


class Traductor(Form):
    espaniol = StringField('Español',
    [validators.DataRequired('El Campo es requerido')])
    ingles =StringField('Ingles',
    [validators.DataRequired('El Campo es requerido')])
    

class LoginForm(Form):
    username=StringField('usuario',
    [validators.DataRequired('El Campo Usuario es requerido'),
     validators.length(min=5,max=10,message='Ingresa min 5 max 10')])
    password=PasswordField('contraseña',
    [validators.DataRequired('El Campo Contraseña es requerido'),
     validators.length(min=5,max=10,message='Ingresa min 5 max 10')])
    
