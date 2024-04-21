from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from utils import error_resp, success_resp

index = Blueprint('index', __name__, static_folder='static', template_folder='templates')


@index.route('/')
def home():
    return render_template('index.html')

@index.route('/scans')
def show_scans():
    return render_template('general_scans.html')

@index.route('/auth', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def auth():
    # For getting user info
    if request.method == 'GET':
        if current_user.is_authenticated:
            return {'netid': current_user.netid, 'name': current_user.name, 'type': current_user.type}
        return jsonify({'netid': None, 'name': None, 'type': None})

    # For logging in
    elif request.method == 'POST':
        netid = request.form.get('netid')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(netid=netid).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
        return redirect(url_for('underground.underground_home'))

    # For changing password
    elif request.method == 'PATCH':
        if current_user.is_authenticated:
            old_password = request.form.get('old_password')
            password = request.form.get('new_password')
            if check_password_hash(current_user.password, old_password):
                user = User.query.filter_by(netid=current_user.netid).first()
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


@index.route('/auth/logout')
def logout():
    logout_user()
    return redirect(url_for('underground.underground_home'))