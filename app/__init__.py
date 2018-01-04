# -*- coding:utf-8 -*-
from flask import Flask, render_template,session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_session import Session
from flask_cache import Cache

from celery import Celery
from config import Config


bootstrap = Bootstrap()
db = SQLAlchemy()
config = Config()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = None
mail = Mail()
celery = Celery(__name__, broker=config.CELERY_BROKER_URL)
moment = Moment()
sess = Session()
cache = Cache()

# 程序初始化
def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  #csf

    bootstrap.init_app(app)
    db.init_app(app)
    config.init_app(app)
    sess.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    cache.init_app(app)

    #初始化celery
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .tasks import tasks as tasks_blueprint
    app.register_blueprint(tasks_blueprint)


    return app