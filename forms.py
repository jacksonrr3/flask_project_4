from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired, Length, Email


class RegistrationForm(FlaskForm):

    username = StringField("Электропочта:", [InputRequired(message="Необходимо указать логин"),
                                             Email(message="Необходимо указать email в качестве логина")])
    password = PasswordField("Пароль:", [InputRequired(message="Необходимо задать пароль"),
                                         Length(min=5, message="Пароль не менее 5 символов")])
    confirm_password = PasswordField("Повторите пароль", [InputRequired(message="Необходимо повторить пароль")])

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):

    username = StringField("Электропочта:", [InputRequired(message="Необходимо указать логин"),
                                             Email(message="Необходимо указать email в качестве логина")])

    password = PasswordField("Пароль:", validators=[InputRequired(message="Необходимо ввести пароль")])

    submit = SubmitField('Войти')


class OrderForm(FlaskForm):

    name = StringField("Ваше имя:", [InputRequired(message="Необходимо указать имя")])

    address = StringField("Адрес:", [InputRequired(message="Необходимо указать имя")])

    mail = StringField("Электропочта:", [InputRequired(message="Необходимо указать почту"),
                                         Email(message="Необходимо указать email в качестве логина")])

    phone = StringField("Ваш телефон",
                        validators=[InputRequired(message="Необходимо указать телефон"),
                                    Length(min=7, max=15, message="Номер должен быть от 7 до 15-ти цифр")])

    submit = SubmitField('Оформить заказ')
