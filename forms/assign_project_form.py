from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class AssignProjectForm(FlaskForm):
    user_id = SelectField('Пользователь', coerce=int, validators=[DataRequired()])
    project_id = SelectField('Проект', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Назначить')