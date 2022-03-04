from flask_wtf import FlaskForm
from .models import User
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, ValidationError


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email.')])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Regexp(
                '^(?=\S{6,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])',
                message='The password must contain at least: ' \
                        'Uppercase characters, ' \
                        'lowercase characters, ' \
                        'digits, ' \
                        'special characters.'
                )
        ]
    )
    confirm = PasswordField(
        'Confirm',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Sign Up')


class LogInForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email(message='Invalid email.')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class EditProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email.')])

    # TODO about, preferences

    submit = SubmitField('Edit Profile')


    def __init__(self, current_username, current_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.current_username = current_username
        self.current_email = current_email


    def validate_username(self, username):
        if username.data != self.current_username:
            user = User.query.filter_by(username=self.username.data).first()

            if user is not None:
                raise ValidationError('Username already in use.')


    def validate_email(self, email):
        if email.data != self.current_email:
            user = User.query.filter_by(email=self.email.data).first()

            if user is not None:
                raise ValidationError('Email already in use.')


class RequestNewPasswordForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email(message='Invalid email.')])
    submit = SubmitField('Send')

#TODO refactor

class SetNewPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Regexp(
                '^(?=\S{6,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])',
                message='The password must contain at least: ' \
                        'Uppercase characters, ' \
                        'lowercase characters, ' \
                        'digits, ' \
                        'special characters.'
                )
        ]
    )
    confirm = PasswordField(
        'Confirm',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Set Password')