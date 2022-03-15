from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.project.forms import NewProjectForm, EditProjectForm, AddCollaboratorsForm
from app.auth.models import User
from app.project.models import Project, Team
from app.helpers.mail import send_project_invitation
from app import db
from datetime import datetime

project_bp = Blueprint('project',
                       __name__,
                       static_folder='static',
                       template_folder='templates',
                       static_url_path="/project/static")

@project_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
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
            return redirect(url_for('project.all'))

        flash('Project name already exists.', category='warning')

    return render_template('new.html',
                           form=form,
                           title='New project')


@project_bp.route('/')
@login_required
def all():
    projects_owner = current_user.projects_owner
    projects_guest = current_user.projects_guest

    return render_template('all.html',
                           title='Projects',
                           projects_owner=projects_owner,
                           projects_guest=projects_guest)


@project_bp.route('project/<uuid:project_id>', methods=['GET', 'POST'])
@login_required
def show(project_id):
    project = Project.query.get(project_id)
    form = AddCollaboratorsForm()
    form.subjects.choices = [(str(user.id), user.username) for user in User.query.all() if user != current_user]

    if form.validate_on_submit():
        subjects = form.subjects.data
        print(subjects)

        # if collaborator:
        #     if collaborator not in project.collaborators:
        #         send_project_invitation(project, collaborator)
        #         return {'success': True, 'msg': 'ok'}
        #     else:
        #         msg = 'User alredy invited.'
        # else:
        #     msg = 'User not found.'
        # return {'success': False, 'msg': msg}

    if project in current_user.projects:
        return render_template('show.html',
                               title=project.project_name,
                               project=project,
                               form=form)

    flash('No project found!', category='warning')
    return redirect(url_for('project.all'))


@project_bp.route('delete/<uuid:project_id>')
@login_required
def delete(project_id):
    project = Project.query.get(project_id)

    if current_user.is_owner(project):
        db.session.delete(project)
        db.session.commit()
        flash(f'Project {project.project_name} successfully deleted.', category='success')
    else:
        flash('No project found!', category='warning')

    return redirect(url_for('project.all'))


@project_bp.route('/edit/<uuid:project_id>', methods=['GET', 'POST'])
@login_required
def edit(project_id):
    form = EditProjectForm()
    project = Project.query.get(project_id)

    if current_user.is_owner(project):
        if form.validate_on_submit():
            project.project_name = form.project_name.data
            project.project_desc = form.project_desc.data
            project.updated_at = datetime.utcnow()

            db.session.commit()
            flash('Your changes have been saved.', category='success')

            return redirect(url_for('project.all'))
        else:
            form.project_name.data = project.project_name
            form.project_desc.data = project.project_desc

            return render_template('edit.html',
                                   form=form,
                                   title='Edit Project')

    flash('No project found!', category='warning')
    return redirect(url_for('project.all'))


@project_bp.route('project/collaborator/<token>')
def add_collaborator(token):
    try:
        project_id, user_id = Project.project_collaborator_token(token)
        project = Project.query.get(project_id)
        user = User.query.get(user_id)

        db.session.add(Team(project=project, user=user))
        db.session.commit()

        flash(f'Great! You are now collaborating with {project.project_name!r}', category="success")
    except Exception as e:
        flash('Expired/invalid token!', category='danger')

    return redirect(url_for('home.workspace'))