from flask import Blueprint, render_template
from flask_login import login_required


home = Blueprint('home',
                    __name__,
                    static_folder='static',
                    template_folder='templates')


@home.route('/')
def index():
    return render_template('home.html')

