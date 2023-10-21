from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileAllowed

from models.categories import Category

class CreateProductForm(FlaskForm):  
    categories = Category.get_all()
    cats = [(-1, '')]
    for cat in categories:
        cats.append((cat.id, cat.category))
    
    name = StringField('Nombre', 
                           validators=[DataRequired('Este campo es necesario.')])
    price = FloatField('Precio',
                                validators=[DataRequired(), NumberRange(min=0.0, max=None)])
    stock = IntegerField('Existencia',
                                validators=[DataRequired(), NumberRange(min=0.0, max=None)])
    size = IntegerField('Tamaño',
                                validators=[DataRequired()])
    category_id = SelectField('Categoría',
                              choices=cats, coerce=int, validate_choice=False, validators=[DataRequired()])
    image = FileField('Imagen de producto', 
                      validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo imagenes!')])
    submit = SubmitField('Guardar')
    
    
class UpdateProductForm(FlaskForm):
    
    # categories = Category.get_all()
    cats = []
    # for cat in categories:
    #     cats.append((cat.id, cat.category))

    name = StringField('Nombre', 
                       validators=[DataRequired()])
    price = FloatField('Precio', 
                       validators=[DataRequired(), NumberRange(min=0.0, max=None)])
    stock = IntegerField('Existencias', 
                         validators=[DataRequired(), NumberRange(min=0, max=None)])
    size = IntegerField('Tamaño',
                        validators=[DataRequired()])
    category_id = SelectField('Categoría', 
                              choices=cats, coerce=int, validate_choice=False, validators=[DataRequired()])
    image = FileField('Imagen de Ingrediente', 
                      validators=[FileAllowed(['jpg', 'png', 'jpeg', 'jfif'], 'Solo imagenes!')])
    submit = SubmitField('Actualizar')