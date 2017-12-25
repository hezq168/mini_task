# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from app import celery, create_app


app = create_app()
app.app_context().push()