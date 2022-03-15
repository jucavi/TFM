from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired

class ProjectBasicForm(FlaskForm):
    project_name = StringField('Project name', validators=[DataRequired()])
    project_desc = TextAreaField('Project description', validators=[DataRequired()])

    submit = SubmitField()


class NewProjectForm(ProjectBasicForm):
    submit = SubmitField('Create Project')


class EditProjectForm(ProjectBasicForm):
    submit = SubmitField('Edit Project')


class AddCollaboratorsForm(FlaskForm):
    subjects = SelectMultipleField()
    submit = SubmitField('Add people')