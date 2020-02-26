from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from werkzeug.security import generate_password_hash


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
        return render_template('users/new.html', message = success)
    else:
        success = False
        return render_template('users/new.html', message = success, errors=user.errors)
    
    


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
