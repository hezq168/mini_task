# -*- coding:utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = True
    SESSION_TYPE = 'filesystem'
    SECRET_KEY = '######################'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
#   mysql自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#   mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xxx:xxxx@127.0.0.1/xxx?charset=utf8'
#   打印sql
    SQLALCHEMY_ECHO = True
#   邮件配置
    MAIL_SERVER = '###############'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEBUG = True
    MAIL_USERNAME = '####################'
    MAIL_PASSWORD = '###################'
    MAIL_SENDER = '#############'


#   celery配置
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_ALWAYS_EAGER = True
    CELERYBEAT_SCHEDULE = {
        'TimedTask': {
           'task': 'app.tasks.printy.TimedTask',
           'schedule': crontab(minute=35, hour=11),
           'args': ()
        },
    }
#   celery时区
    CELERY_TIMEZONE = 'Asia/Shanghai'

#   文章分页数
    POSTS_PER_PAGE = 15


    @staticmethod
    def init_app(app):
        pass
