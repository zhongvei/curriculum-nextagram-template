from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from models.user_images import Image
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from flask_login import login_user, current_user, login_required, current_user
from helpers import *


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
    return render_template('users/users.html', user=user)

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    if str(current_user.id) == id:
        return render_template('users/edit.html')
    return current_user.id



@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)
    email = request.form.get('email')
    name = request.form.get('username')
    user.email = email
    user.name = name
    user.save()
    return redirect(url_for('users.edit', id=user.id))

@users_blueprint.route('/upload', methods=["POST"])
@login_required
def upload_img():
    file = request.files["user_file"]
    user = User.get_or_none(User.id == current_user.id)
    if user:
        if file :
            file.filename = secure_filename(file.filename)
            output   	  = upload_file_to_s3(file)
            if str(output) == 'None':
                user.image_path = file.filename
                user.save()
                return redirect(url_for('home'))
            else:
                return redirect(url_for('home'))
        else:
            return redirect("/")
    else:
        return redirect("/")
    return render_template('/users/profile.html')

@users_blueprint.route('/<username>/upload_my_image', methods= ['POST'])
@login_required
def upload_my_image(username):
    file = request.files["user_file"]
    user = User.get_or_none(User.id == current_user.id)
    image = Image(image_path = file.filename, user_id = user.id)
    upload_file_to_s3(file)
    image.save()
    return redirect(url_for('users.show', username = username))
