from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email


class MessageForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email.')])
    message = TextAreaField('Message',
                            validators=[DataRequired(), Length(min=0, max=140)])
    submit = SubmitField('Submit')