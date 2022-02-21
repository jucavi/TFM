from flask import Blueprint, flash, redirect, render_template, url_for, request
from project import login_manager, db
from .user_model import User
from .forms import EditProfileForm, LogInForm, SignUpForm
from flask_login import current_user, login_required, login_user, logout_user


auth_bp = Blueprint('auth', __name__, static_folder='static', template_folder='templates')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        db_user = User.query.filter_by(email=form.email.data).first()
        if not db_user:
            firstname = form.firstname.data
            lastname = form.lastname.data
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm = form.confirm.data

            if password == confirm:
                user = User(
                    firstname=firstname,
                    lastname=lastname,
                    username=username,
                    email=email,
                )
                user.set_password(password)

                db.session.add(user)
                db.session.commit()

                login_user(user)
                return redirect(url_for('auth.login'))

        flash('User already exists!')
    return render_template('auth/signup.html', form=form, title='Sign Up', header='Sign Up')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.workspace'))

    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home.workspace'))

        flash('Invalid username/password.', category='warning')

    return render_template('auth/login.html', form=form, title='Log In')



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(current_user.username, current_user.email)

    if form.validate_on_submit():
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()
        flash('Your changes have been saved.', category='success')
        return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('auth/profile.html', form=form, title='Edit Profile', header='Edit Profile')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in.', category='warning')
    return redirect(url_for('auth.login'))
