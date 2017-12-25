# -*- coding:utf-8 -*-
__author__ = 'Administrator'

from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,SubmitField,DateTimeField,IntegerField,DateField,TextAreaField,SelectMultipleField,SelectField
from wtforms.validators import Length,Email,InputRequired,DataRequired

#任务发布表单
class Addtask(FlaskForm):
    task_name = StringField(u'任务名：',validators=[DataRequired(message=u"任务名不能为空"),Length(1,64)])
    duty = SelectField(u'责任人：',validators=[DataRequired()])
    assist = SelectField(u'协助人:',validators=[DataRequired()])
    project = SelectField(u'所属项目:',validators=[DataRequired()])
    priority = SelectField(u'优先级:',validators=[DataRequired()],choices=[('中','中'),('高','高'),('低','低')])
    task_type = SelectField(u'任务类型:',validators=[DataRequired()],choices=[('开发','开发'),('维护','维护'),('支持','支持')])
    department = SelectField(u'任务部门:',validators=[DataRequired()])
    text = TextAreaField(u'任务描述:',validators=[DataRequired(message=u"任务描述不能为空")])
    submit = SubmitField(u'提交')





#修改任务
class EditTask(FlaskForm):
    task_name = StringField(u'任务名：',validators=[DataRequired(message=u"任务名不能为空"),Length(1,64)])
    duty = SelectField(u'责任人：',validators=[DataRequired()])
    assist = SelectField(u'协助人:',validators=[DataRequired()])
    project = SelectField(u'所属项目:',validators=[DataRequired()])
    priority = SelectField(u'优先级:',validators=[DataRequired()],choices=[('中','中'),('高','高'),('低','低')])
    task_type = SelectField(u'任务类型:',validators=[DataRequired()],choices=[('开发','开发'),('维护','维护'),('支持','支持')])
    department = SelectField(u'任务部门:',validators=[DataRequired()])
    text = TextAreaField(u'任务描述:',validators=[DataRequired(message=u"任务描述不能为空")])
    start_time = DateTimeField(u'开始时间:')
    end_time = DateTimeField(u'结束时间:')
    submit = SubmitField(u'修改')



#定议一个分页表单
class PostForm(FlaskForm):
    post = StringField('post',validators=[DataRequired()])



#任务搜索表单
class SearchTask(FlaskForm):
    search_task = StringField(u'' , validators=[DataRequired(message=u'内容不能为空')])
    submit = SubmitField(u'搜索')


#回复表单内容
class TaskContent(FlaskForm):
    text = TextAreaField(u'回复内容',validators=[DataRequired(message=u'回复内容不能为空')])
    submit = SubmitField(u'回复')
