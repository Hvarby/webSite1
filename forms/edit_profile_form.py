from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Новый пароль')
    confirm_password = PasswordField('Повторите пароль', validators=[EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Сохранить')