from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, FieldList
from wtforms.validators import DataRequired, Length


class MessageForm(FlaskForm):
    recipients = FieldList(StringField(), validators=[DataRequired(message='Email required.')])
    subject = StringField('Subject',
                          validators=[DataRequired(message='Subject required.'), Length(min=0, max=100, message='No more than 100 characters')])
    body = TextAreaField('Body',
                            validators=[DataRequired(message='Empty message.')])
    submit = SubmitField('Submit')