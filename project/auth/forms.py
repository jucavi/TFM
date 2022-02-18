from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp

class SignUpForm(FlaskForm):
    firstname = StringField(
        'First Name',
        validators=[DataRequired()]
    )
    lastname = StringField(
        'Last Name',
        validators=[DataRequired()]
    )
    username = StringField(
        'Username',
        validators=[DataRequired()]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Invalid email.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Regexp(
                '^(?=\S{6,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])',
                message='The password must contain at least:' \
                        'Uppercase characters, ' \
                        'lowercase characters,' \
                        'digits,' \
                        'special characters.'
                )
        ]
    )
    confirm = PasswordField(
        'Password confirmation',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Sign Up')


class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class ProfileForm(FlaskForm):
    pass
