from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.project.forms import NewProjectForm, EditProjectForm, AddCollabForm, UploadFileForm
from app.auth.models import User
from app.project.models import Project, Team, Folder, File, FolderContent
from app.helpers.mail import send_email, send_project_invitation
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

    return render_template('new.html',
                           action='Create new project',
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
    collab_form = AddCollabForm()
    emails = {'elements': [user.email for user in User.query.all() if user != current_user]}

    if project in current_user.projects:
        folder = project.root_folder

        if collab_form.validate_on_submit():
            print('send')
            print(collab_form.collabs.data)
            for email in collab_form.collabs.data:
                print(email)
                collab = User.query.filter_by(email=email).first()
                print(collab)
                if collab:
                    if collab not in project.collaborators:
                        send_project_invitation(project, collab)
                        flash(f'Invitation sed to {email!r}.', category='success')
                    else:
                        flash(f'{email!r} already collaborate.', category='info')
                else:
                    flash(f'{email!r} not found.', category='danger')

        return render_template('show.html',
                               title=project.project_name,
                               project=project,
                               collab_form=collab_form,
                               hidden_elements=json.dumps(emails),
                               folder=folder)


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
                # if project_name change change root folder name change too
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

            return render_template('new.html',
                                   action='Edit project',
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
            return redirect(url_for('projects.show_project', project_id=project_id))
        else:
            raise Exception

    except Exception:
        flash('Expired/invalid access token!', category='danger')

    return redirect(url_for('projects.all_projects'))



@projects.route('project/<uuid:project_id>/data/<folder_id>')
@login_required
def show_folder_content(project_id, folder_id):
    project = Project.query.get_or_404(project_id)

    if project in current_user.projects:
        folder = Folder.query.get_or_404(folder_id)
        return folder.toJSON()

    return {'success': False, 'msg': 'No project found.'}


@projects.route('project/<uuid:project_id>/folder/<folder_id>', methods=['PUT', 'POST', 'DELETE'])
@login_required
def op_folder(project_id, folder_id):
    project = Project.query.get_or_404(project_id)
    folder = Folder.query.get_or_404(folder_id)
    name = request.form.get('name')

    if project.has_access(current_user, folder):
        if request.method == 'DELETE' and folder.id != project.root_folder.id:
            db.session.delete(folder)
            msg = 'Successfully deleted.'


        elif folder.is_valid_folder(name):
            if request.method == 'POST':
                db.session.add(Folder(foldername=name, project=project, parent=folder))
                msg = 'Successfully created.'

            elif request.method == 'PUT' and folder.id != project.root_folder.id:
                folder.foldername = name
                msg = 'Successfully renamed.'
        else:
            return {'success': False, 'msg': 'Invalid name.' }

        db.session.commit()
        return {'success': True, 'msg': msg}

    return {'success': False, 'msg': 'Access denied.' }



@projects.route('project/<uuid:project_id>/<folder_id>/files')
@login_required
def files(project_id, folder_id):
    project = Project.query.get_or_404(project_id)
    folder = Folder.query.get_or_404(folder_id)
    form = UploadFileForm()

    if project.has_access(current_user, folder):
        files = folder.files
    else:
        flash('Access denied.')
        return redirect(url_for('projects.show_project', project_id=project.id))

    return render_template('files.html',
                           files=files,
                           form=form,
                           project=project,
                           folder=folder)


@projects.route('/project/<uuid:project_id>/<uuid:folder_id>/files/upload', methods=['POST'])
def upload_files(project_id, folder_id):
    project = Project.query.get_or_404(project_id)
    folder = Folder.query.get_or_404(folder_id)

    try:
        upload = request.files['file']
        print(upload)
        print(upload.mimetype)
        print(upload.name)
        print(upload.content_type)
        print(upload.content_length)
        print(upload.__sizeof__())
        print(dir(upload))
        name = upload.filename
        data = upload.read()
        if project.has_access(current_user, folder):
            if folder.is_valid_file(name):
                pass
                # file = File(filename=name, data=data)
                # FolderContent(folder=folder, file=file)
                # db.session.add(file)
                # db.session.commit()
            else:
                flash('Invalid name or file already exists.')
        else:
            flash('Access denied')
    except Exception as e:
        print(e)

    return redirect(url_for('projects.files',
                            project_id=project_id,
                            folder_id=folder.id))