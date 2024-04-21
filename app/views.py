from flask import Blueprint, render_template

index = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index.route('/')
def home():
    return render_template('home.html')

@index.route('/scans')
def show_scans():
    return render_template('general_scans.html')
