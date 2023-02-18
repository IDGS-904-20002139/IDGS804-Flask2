from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.fields import FieldList

class CajaForm(Form):
    ncontent = IntegerField('Contenedores')
    numero = FieldList(StringField('numero'), min_entries=1)
