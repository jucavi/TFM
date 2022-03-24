from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.project.forms import NewProjectForm, EditProjectForm, AddCollabForm
from app.auth.models import User
from app.project.models import Project, Team, Folder, File, FolderContent
from app.helpers.mail import send_project_invitation
from app import db
import json
from datetime import datetime
from sqlalchemy.exc import IntegrityError

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
        try:
            project = Project(project_name, project_desc)
            user = current_user

            team = Team(project=project, user=user, is_owner=True)

            db.session.add(team)
            db.session.commit()

            flash('Project successfully created.', category='success')
            return redirect(url_for('projects.all_projects'))
        except IntegrityError:
            db.session.rollback()
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
    project = Project.query.get_or_404(project_id)
    form = AddCollabForm()
    emails = {'elements': [user.email for user in User.query.all() if user != current_user]}

    if form.validate_on_submit():
        for email in form.collabs.data:
            collab = User.query.filter_by(email=email).first()
            if collab:
                if collab not in project.collaborators:
                    send_project_invitation(project, collab)
                    flash(f'Invitation sed to {email!r}.', category='success')
                else:
                    flash(f'{email!r} already collaborate.', category='info')
            else:
                flash(f'{email!r} not found.', category='danger')

    if project in current_user.projects:
        root = project.root_folder
        return render_template('project.html',
                               title=project.project_name,
                               project=project,
                               form=form,
                               hidden_elements=json.dumps(emails),
                               root=root)

    flash('No project found!', category='warning')
    return redirect(url_for('projects.all_projects'))


@projects.route('delete/<uuid:project_id>')
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

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
    project = Project.query.get_or_404(project_id)
    root = project.root_folder

    if current_user.is_owner(project):
        if form.validate_on_submit():
            try:
                project_name = form.project_name.data
                # if project_name change change root folder name too
                root.foldername = project_name

                project.project_name = project_name
                project.project_desc = form.project_desc.data
                project.updated_at = datetime.utcnow()

                db.session.add(root)
                db.session.commit()

                flash('Your changes have been saved.', category='success')
                return redirect(url_for('projects.all_projects'))
            except IntegrityError:
                db.session.rollback()
                flash('Proyect name already exists.', category='danger')
                return redirect(url_for('projects.edit_project', project_id=project_id))
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
        project = Project.query.get_or_404(project_id)
        user = User.query.get_or_404(user_id)

        if user == current_user:
            db.session.add(Team(project=project, user=user))
            db.session.commit()

            flash(f'Great! You are now collaborating with {project.project_name!r}', category="success")
        else:
            raise Exception

    except Exception:
        flash('Expired/invalid access token!', category='danger')

    return redirect(url_for('home.index'))


@projects.route('project/<uuid:project_id>/data/<folder_id>')
@login_required
def show_folder_content(project_id, folder_id):
    project = Project.query.get_or_404(project_id)

    if project in current_user.projects:
        folder = Folder.query.get_or_404(folder_id)
        return folder.toJSON()


@projects.route('project/<uuid:project_id>/folder/<parent_id>')
@login_required
def new_folder(project_id, parent_id):
    project = Project.query.get_or_404(project_id)
    parent = Folder.query.get_or_404(parent_id)
    name = request.args.get('name')

    if project in current_user.projects and parent.project == project and name:
        db.session.add(Folder(foldername=name, project=project, parent=parent))
        db.session.commit()

    return redirect(url_for('projects.show_project', project_id=project.id))


@projects.route('project/<uuid:project_id>/file/<parent_id>')
@login_required
def new_file(project_id, parent_id):
    project = Project.query.get_or_404(project_id)
    parent = Folder.query.get_or_404(parent_id)
    name = request.args.get('name')

    if project in current_user.projects and parent.project == project and name:
        file = File(filename=name)

        db.session.add(FolderContent(folder=parent, file=file))
        db.session.commit()

    return redirect(url_for('projects.show_project', project_id=project.id))
