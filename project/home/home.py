from flask import Blueprint, render_template, flash

home_bp = Blueprint('home', __name__, static_folder='static', template_folder='templates')


@home_bp.route('/')
def home():
    flash('This is a error', category='danger')
    return render_template('home.html')