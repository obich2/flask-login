from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    hashed_password = StringField('Пароль', validators=[DataRequired()])
    password_again = StringField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')