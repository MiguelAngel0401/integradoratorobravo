from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CreatePromotionForm(FlaskForm):
    name = StringField('Nombre', 
                           validators=[DataRequired()])
    description = TextAreaField('Descripcion',
                                validators=[DataRequired()])
    submit = SubmitField('Guardar')
    
class UpdatePromotionForm(FlaskForm):
    name = StringField('Nombre', 
                           validators=[DataRequired()])
    description = TextAreaField('Descripcion',
                                validators=[DataRequired()])
    submit = SubmitField('Guardar')