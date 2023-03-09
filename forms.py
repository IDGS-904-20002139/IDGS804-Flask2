from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, RadioField
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
    
class ResistenciasForm(Form):
    colores = [('', '---'),
              ('0', 'Negro'), 
              ('1', 'Marron'),
              ('2', 'Rojo'),
              ('3', 'Naranja'), 
              ('4', 'Amarillo'), 
              ('5', 'Verde'),
              ('6', 'Azul'),
              ('7', 'Violeta'), 
              ('8', 'Gris'), 
              ('9', 'Blanco')]
    banda1 = SelectField('Banda 1', choices=colores, validators=[validators.DataRequired('Llena el siguiente campo')])
    banda2 = SelectField('Banda 2', choices=colores, validators=[validators.DataRequired('Llena el siguiente campo')])
    multiplier = SelectField('Banda 3 multiplicadora', choices=[('', '---'), ('0', 'Negro x1 Ω'), ('1', 'Marron x10 Ω'), 
                                              ('2', 'Rojo x100 Ω'), ('3', 'Naranja x1000 Ω'),
                                              ('4', 'Amarillo x10,000 Ω'), ('5', 'Verde x100,000 Ω'), 
                                              ('6', 'Azul x1,000,000 Ω'), ('7', 'Violeta x10,000,000 Ω'),
                                              ('8', 'Gris x100,000,000 Ω'), ('9', 'Blanco x1,000,000,000 Ω')],
                                                       validators=[validators.DataRequired()])
    tolerancia = RadioField('Elige la tolerancia', choices=[('oro', 'ORO = x0,1 Ω (5%)'), ('plata', 'PLATA = x0,01 Ω (10%)')], 
                           validators=[validators.DataRequired(message='Llena el siguiente campo')])