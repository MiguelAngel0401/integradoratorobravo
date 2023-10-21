from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class CreateSellForm(FlaskForm):  
    prod_name = StringField('Producto', 
                           validators=[DataRequired(), NumberRange(min=0.0, max=None)])
    tProduct = IntegerField('Total producto', 
                           validators=[DataRequired()])
    submit = SubmitField('Generar Orden')
    
    