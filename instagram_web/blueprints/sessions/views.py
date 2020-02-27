from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, current_user, logout_user
from app import app

login_manager = LoginManager()
login_manager.init_app(app)

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    if current_user.is_authenticated:
        return render_template('sessions/new.html')
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def create():
    if current_user.is_authenticated:
        return render_template('sessions/new.html')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.get_or_none(User.email == email)

    if user:
        if check_password_hash(user.password, password):
            login_user(user)
            return render_template('sessions/new.html',access=True)
        else:
            return render_template('sessions/new.html',access=False, message='Invalid Password')
    else:
        return render_template('sessions/new.html', access=False, message='Invalid email address')

@sessions_blueprint.route('/logout')
def logout():
    logout_user()
    return render_template('sessions/new.html')