from flask import Blueprint, render_template, request, jsonify, redirect, url_for, Markup, abort
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Report
from utils import error_resp, success_resp
import re
import os
import markdown

index = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index.route('/', methods=['GET','POST'])
def home():
    login = current_user.is_authenticated
    if request.method == 'GET':
        return render_template('home.html', login=login)
    # elif request.method == "POST":
    #     ip = request.form.get('ip')



@index.route('/scans')
def show_scans():
    login = current_user.is_authenticated
    if login:
        return render_template('general_scans.html', login=login)
    else:
        return error_resp('Must be logged in to see scans')

@index.route('/login')
def login():
    login = current_user.is_authenticated
    if login:
        return redirect(url_for('index.home'))
    return render_template('login.html',
                           login=login,
                           name=current_user.username if login else None,
                           )

@index.route('/auth', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def auth():
    # For getting user info
    if request.method == 'GET':
        if current_user.is_authenticated:
            return {'Username': current_user.username}
        return jsonify({'username': None})

    # For logging in
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('index.home'))
        return redirect(url_for('index.login'))

    # For changing password
    elif request.method == 'PATCH':
        if current_user.is_authenticated:
            old_password = request.form.get('old_password')
            password = request.form.get('new_password')
            if check_password_hash(current_user.password, old_password):
                user = User.query.filter_by(username=current_user.username).first()
                user.password = generate_password_hash(password, method='pbkdf2:sha256')
                db.session.add(user)
                db.session.commit()
                return success_resp('Password updated')
            return error_resp('Current password is incorrect')
        return error_resp('Unauthenticated')

    # For logging out
    elif request.method == 'DELETE':
        logout_user()
        return success_resp('Logged out')


@index.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.home'))

@index.route("/register", methods=['GET', 'POST'])
def register():
    login = current_user.is_authenticated
    if not login:
        return abort(401)
    if request.method == "GET":
        return render_template("register.html", login=login)
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        passwordSecond = request.form.get("password2")
        if not (username and password and passwordSecond):
            return render_template("register.html", registerError = "Please complete all the fields", login=login)
        if password != passwordSecond:
            return render_template("register.html", registerError = "Passwords do not match")
        if len(password) < 8 or not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
            registerError = "<div class='text-start'>Password do not meet the requirements:\
            \n<ul><li>Password needs to have at least 8 characters</li>\
            \n<li>Password needs to contain at least one letter</li>\
            \n<li>Password needs to contain at least one number</li></ul></div>";
            return render_template("register.html", registerError = registerError, login=login)
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template("register.html", registerError = "This username has already been taken, please try a different username", login=login)
        newUser = User(
            username=username,
            password=generate_password_hash(password, "pbkdf2:sha256")
            )
        # with app.app_context():
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('index.home')) 

@index.route("/unregister", methods=["GET", "POST"])
def unregister():
    return None

@index.route('/reports/<id>')
def show_report(id):
    """
    Renders a webpage that displays the report with the specified id.
    args:
        id: The id field of the report in the database
    """
    login = current_user.is_authenticated
    if not login:
        return abort(401)
    report = Report.query.filter_by(id=id).first()
    if not report:
        return abort(404)
    report_markdown = report.content
    report_html = markdown.markdown(report_markdown, extensions=['tables', "sane_lists"])
    report_html = report_html.replace("<table>", '<table class="table">')
    report_html = Markup(report_html)
    return render_template('report.html', report=report_html, login=login)

@index.route("/reports")
def list_reports():
    """Renders a webpage with a list of reports"""
    login = current_user.is_authenticated
    if not login:
        return abort(401)
    reports = Report.query.all()
    ret = []
    if reports:
        ret = [(report.id, report.ip, report.time.strftime("%Y-%M-%D"), report.time.strftime("%H:%M:%S")) for report in reports]
    message = ""
    if len(ret) == 0:
        message = "You have not done any scan"
    return render_template('report_list.html', report_names=ret, message=message, login=login)
