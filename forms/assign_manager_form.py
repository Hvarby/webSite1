from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class AssignManagerForm(FlaskForm):
    subordinate_id = SelectField('Сотрудник', coerce=int, validators=[DataRequired()])
    manager_id = SelectField('Руководитель', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Назначить руководителя')