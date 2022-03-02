from flask import Blueprint, render_template
from flask_login import login_required


home_bp = Blueprint(
    'home',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@home_bp.route('/')
def home():
    return render_template('home.html')


@home_bp.route('/workspace')
@login_required
def workspace():
    return render_template('workspace.html')


@home_bp.route('/<_>')
def missing_route(_):
    return render_template('home.html')
