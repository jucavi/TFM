from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FieldList
from wtforms.validators import DataRequired

class ProjectBasicForm(FlaskForm):
    project_name = StringField('Project name', validators=[DataRequired()])
    project_desc = TextAreaField('Project description', validators=[DataRequired()])

    submit = SubmitField()


class NewProjectForm(ProjectBasicForm):
    submit = SubmitField('Create Project')


class EditProjectForm(ProjectBasicForm):
    submit = SubmitField('Edit Project')


class AddCollabForm(FlaskForm):
    collabs = FieldList(StringField())
    submit = SubmitField('Add People')