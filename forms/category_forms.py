from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CreateCategoryForm(FlaskForm):
    category = StringField('Categoria', 
                           validators=[DataRequired()])
    description = TextAreaField('Descripcion',
                                validators=[DataRequired()])
    submit = SubmitField('Guardar')
    
class UpdateCategoryForm(FlaskForm):
    category = StringField('Categoria', 
                           validators=[DataRequired()])
    description = TextAreaField('Descripcion',
                                validators=[DataRequired()])
    submit = SubmitField('Guardar')