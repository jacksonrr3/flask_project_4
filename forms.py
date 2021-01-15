from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length, Email


class RegistrationForm(FlaskForm):

    username = StringField("Email:", [InputRequired(message="Необходимо указать логин"),
                                      Email(message="Необходимо указать email в качестве логина")])
    password = PasswordField("Пароль:", validators=[InputRequired(message="Необходимо задать пароль"),
                                                    Length(min=5, message="Не менее 5 символов")])

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):

    username = StringField("Email:", validators=[DataRequired()])

    password = PasswordField("Пароль:", validators=[DataRequired()])

    submit = SubmitField('Войти')