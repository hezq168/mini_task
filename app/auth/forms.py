# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email

#用户登录from
class LoginFrom(FlaskForm):
    email = StringField('登录邮箱：',validators=[Required(),Length(1,64),Email()])
    password = PasswordField('密码：',validators=[Required()])
    submit = SubmitField('登录')


