from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils import error_resp, success_resp
import re

index = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index.route('/')
def home():
    return render_template('index.html')

@index.route('/scans')
def show_scans():
    return render_template('general_scans.html')

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
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        passwordSecond = request.form.get("password2")
        if not (username and password and passwordSecond):
            return render_template("register.html", registerError = "Please complete all the fields")
        if password != passwordSecond:
            return render_template("register.html", registerError = "Passwords do not match")
        if len(password) < 8 or not re.search("[a-zA-Z]", password) or not re.search("[0-9]", password):
            registerError = "<div class='text-start'>Password do not meet the requirements:\
            \n<ul><li>Password needs to have at least 8 characters</li>\
            \n<li>Password needs to contain at least one letter</li>\
            \n<li>Password needs to contain at least one number</li></ul></div>";
            return render_template("register.html", registerError = registerError)
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template("register.html", registerError = "This username has already been taken, please try a different username")
        newUser = User(
            username=username,
            password=generate_password_hash(password, "pbkdf2:sha256")
            )
        # with app.app_context():
        db.session.add(newUser)
        db.session.commit()
