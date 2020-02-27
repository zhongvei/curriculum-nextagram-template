from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from werkzeug.security import check_password_hash


sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def login_check():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = User().select().where(email=email) 
        return render_template('sessions/new.html',access = True)
    except:
        return render_template('sessions/new.html',access = False)