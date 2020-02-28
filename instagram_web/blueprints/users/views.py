from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from werkzeug.security import generate_password_hash
from flask_login import login_user, current_user 

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    password = request.form.get('password')
    hashed_password = generate_password_hash(password)
    user = User(email=request.form.get('email'), name=request.form.get('username'), password=hashed_password)
    if user.save():
        success = True
        login_user(user)
        return redirect(url_for('home'))
    else:
        success = False
        return render_template('users/new.html', message = success, errors=user.errors)
    
@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.name == username)
    return render_template('users/users.html',user = user)
 

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    if str(current_user.id) == id:
        return render_template('users/edit.html')
    return current_user.id


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(User.id == id)
    email = request.form.get('email')
    name = request.form.get('username')
    user.email = email
    user.name = name
    user.save()
    return redirect(url_for('users.edit', id = user.id))