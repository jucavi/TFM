from flask import Blueprint, flash, redirect, render_template, url_for, request
from app import login_manager, db
from app.auth.models import User
from app.auth.forms import EditProfileForm, LogInForm, SignUpForm, RequestNewPasswordForm, SetNewPasswordForm
from flask_login import current_user, login_required, login_user, logout_user
from app.helpers.mail import send_password_reset_email


auth_bp = Blueprint(
    'auth',
    __name__,
    static_folder='static',
    template_folder='templates',
    static_url_path="/auth/static"
)


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

        flash('User already exists!', category='warning')
    return render_template('signup.html', form=form, title='Sign Up')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.workspace'))

    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)

            return redirect(url_for('home.workspace'))
        flash('Invalid username/password.', category='warning')

    return render_template('login.html', form=form, title='Log In')



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

    return render_template('profile.html', form=form, title='Edit Profile', back=request.referrer)


@auth_bp.route('/request_new_password', methods=['GET', 'POST'])
def request_new_password():
    form  = RequestNewPasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user:
            send_password_reset_email(user)
            flash(f'We sent a recovery link to you at {user.email}', category='success')

            return redirect(url_for('home.home'))
        flash(f'Not user found by {email}!')

    return render_template('request_new_password.html', form=form, title='Reset Password', back=request.referrer)


@auth_bp.route('/new_password/<token>', methods=['GET', 'POST'])
def new_password(token):
    user = User.check_resert_password_token(token)

    if not user:
        flash('Expired/invalid token!', category='danger')
        return redirect(url_for('auth.request_new_password'))

    form  = SetNewPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password have been reset successfully.', category='success')

        return redirect(url_for('auth.login'))

    return render_template('new_password.html', form=form, title='New Password', back=request.referrer)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash('You need to sign in or sign up before continuing.', category='warning')
    return redirect(url_for('auth.login'))
