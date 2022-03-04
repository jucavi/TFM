from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.project.forms import NewProjectForm, EditProjectForm
from app.project.models import Project, Team
from app import db

project_bp = Blueprint(
    'project',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path="/project/static"
)

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
    return render_template('new.html', form=form, title='New project')


@project_bp.route('/')
@login_required
def all():
    projects_owner = current_user.projects_owner
    projects_guest = current_user.projects_guest

    return render_template(
        'all.html',
        title='Projects',
        projects_owner=projects_owner,
        projects_guest=projects_guest
    )

@project_bp.route('project/<uuid:project_id>')
@login_required
def view(project_id):
    project = Project.query.get(project_id)

    if current_user.is_owner(project):
        return render_template(
            'view.html',
            title=f'Project {project.project_name}',
            project=project
        )

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


@project_bp.route('project/edit/<uuid:project_id>', methods=['GET', 'POST'])
@login_required
def edit(project_id):
    form = EditProjectForm()
    project = Project.query.get(project_id)

    if current_user.is_owner(project):
        if form.validate_on_submit():
            project.project_name = form.project_name.data
            project.project_desc = form.project_desc.data

            db.session.commit()
            flash('Your changes have been saved.', category='success')

            return redirect(url_for('project.all'))
        else:
            form.project_name.data = project.project_name
            form.project_desc.data = project.project_desc

            return render_template('edit.html', form=form, title='Edit Project')

    flash('No project found!', category='warning')
    return redirect(url_for('project.all'))
