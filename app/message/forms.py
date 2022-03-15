from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email


class MessageForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(message='Invalid email.')])
    subject = StringField('Subject',
                          validators=[DataRequired(message='Subject required'), Length(min=0, max=100, message='No more than 100 characters')])
    message = TextAreaField('Message',
                            validators=[DataRequired(message='Empty message')])
    submit = SubmitField('Submit')