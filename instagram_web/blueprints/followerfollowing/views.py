from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from flask_login import current_user

followerfollowing_blueprint = Blueprint('followerfollowing',
                            __name__,
                            template_folder='templates')