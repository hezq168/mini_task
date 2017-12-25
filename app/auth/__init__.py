__author__ = 'Administrator'

from flask import Blueprint
auth = Blueprint('auth', __name__)

from . import views