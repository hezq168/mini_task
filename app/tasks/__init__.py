# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask import Blueprint

tasks = Blueprint('tasks', __name__)

from . import printy

