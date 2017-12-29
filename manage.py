# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from app import create_app, db
from app import models
from app.models import Department
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import send_from_directory, render_template, session
import os

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)





# 创建shell上下文环境
def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()