from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed

class CreateIngredientForm(FlaskForm):
    name = StringField('Nombre', 
                           validators=[DataRequired()])
    marca = StringField('Marca',
                                validators=[DataRequired()])
    size = FloatField('Presentacion',
                                validators=[DataRequired(), NumberRange(min=0.0, max=None)])
    stock = FloatField('Existencia',
                                validators=[DataRequired(), NumberRange(min=0.0, max=None)])
    image = FileField('Imagen de ingrediente', 
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imagenes!')])
    submit = SubmitField('Guardar')
    
class UpdateIngredientForm(FlaskForm):
    name = StringField('Nombre', 
                           validators=[DataRequired()])
    marca = StringField('Marca',
                                validators=[DataRequired()])
    size = FloatField('Presentacion',
                                validators=[DataRequired(), NumberRange(min=0.0, max=None)])
    stock = FloatField('Existencia',
                                validators=[DataRequired(), NumberRange(min=0.0, max=None)])
    image = FileField('Imagen de Producto', 
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imagenes!')])
    submit = SubmitField('Guardar')