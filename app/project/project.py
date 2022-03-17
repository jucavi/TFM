from xml.dom import InvalidAccessErr
from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.project.forms import NewProjectForm, EditProjectForm, AddCollabForm
from app.auth.models import User
from app.project.models import Project, Team
from app.helpers.mail import send_project_invitation
from app import db
import json
from datetime import datetime

projects = Blueprint('projects',
                       __name__,
                       static_folder='static',
                       template_folder='templates',
                       static_url_path="/project/static")

@projects.route('/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = NewProjectForm()

    if form.validate_on_submit():
        project_name = form.project_name.data
        project_desc = form.project_desc.data
        db_project = Project.query.filter_by(project_name=project_name).first()
        if not db_project:
            project = Project(project_name=project_name, project_desc=project_desc)
            user = current_user

            team = Team(project=project, user=user, is_owner=True)

            db.session.add(team)
            db.session.commit()

            flash('Project successfully created.', category='success')
            return redirect(url_for('projects.all_projects'))

        flash('Project name already exists.', category='warning')

    return render_template('new_project.html',
                           form=form,
                           title='New project')


@projects.route('/')
@login_required
def all_projects():
    projects_owner = current_user.projects_owner
    projects_guest = current_user.projects_guest

    return render_template('projects.html',
                           title='Projects',
                           projects_owner=projects_owner,
                           projects_guest=projects_guest)


@projects.route('project/<uuid:project_id>', methods=['GET', 'POST'])
@login_required
def show_project(project_id):
    project = Project.query.get(project_id)
    form = AddCollabForm()
    emails = {'elements': [user.email for user in User.query.all() if user != current_user]}

    if form.validate_on_submit():
        for email in form.collabs.data:
            collab = User.query.filter_by(email=email).first()
            if collab:
                if collab not in project.collaborators:
                    send_project_invitation(project, collab)
                    flash(f'Invitation sed to {email}.', category='success')
                else:
                    flash(f'{email} already collaborate.', category='info')
            else:
                flash(f'{email} not found.', category='danger')

    if project in current_user.projects:
        return render_template('project.html',
                               title=project.project_name,
                               project=project,
                               form=form,
                               hidden_elements=json.dumps(emails))

    flash('No project found!', category='warning')
    return redirect(url_for('projects.all_projects'))


@projects.route('delete/<uuid:project_id>')
@login_required
def delete_project(project_id):
    project = Project.query.get(project_id)

    if current_user.is_owner(project):
        db.session.delete(project)
        db.session.commit()
        flash(f'Project {project.project_name} successfully deleted.', category='success')
    else:
        flash('No project found!', category='warning')

    return redirect(url_for('projects.all_projects'))


@projects.route('/edit/<uuid:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    form = EditProjectForm()
    project = Project.query.get(project_id)

    if current_user.is_owner(project):
        if form.validate_on_submit():
            project.project_name = form.project_name.data
            project.project_desc = form.project_desc.data
            project.updated_at = datetime.utcnow()

            db.session.commit()
            flash('Your changes have been saved.', category='success')

            return redirect(url_for('projects.all_projects'))
        else:
            form.project_name.data = project.project_name
            form.project_desc.data = project.project_desc

            return render_template('edit_project.html',
                                   form=form,
                                   title='Edit Project')

    flash('No project found!', category='warning')
    return redirect(url_for('projects.all_projects'))


@projects.route('project/collaborator/<token>')
@login_required
def add_collaborator(token):
    try:
        project_id, user_id = Project.project_collaborator_token(token)
        project = Project.query.get(project_id)
        user = User.query.get(user_id)

        if user == current_user:
            db.session.add(Team(project=project, user=user))
            db.session.commit()

            flash(f'Great! You are now collaborating with {project.project_name!r}', category="success")
        else:
            raise InvalidAccessErr

    except Exception as e:
        flash('Expired/invalid token!', category='danger')

    return redirect(url_for('home.index'))