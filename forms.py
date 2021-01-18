from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length, Email


class RegistrationForm(FlaskForm):
    username = StringField("Электропочта:", [InputRequired(message="Необходимо указать логин"),
                                             Email(message="Необходимо указать email в качестве логина")])
    password = PasswordField("Пароль:", validators=[InputRequired(message="Необходимо задать пароль"),
                                                    Length(min=5, message="Пароль не менее 5 символов")])

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField("Электропочта:", [InputRequired(message="Необходимо указать логин"),
                                             Email(message="Необходимо указать email в качестве логина")])

    password = PasswordField("Пароль:", validators=[InputRequired(message="Необходимо ввести пароль")])

    submit = SubmitField('Войти')


class OrderForm(FlaskForm):
    username = StringField("Электропочта:", [InputRequired(message="Необходимо указать логин"),
                                             Email(message="Необходимо указать email в качестве логина")])
