# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from app import celery
import sys
import time
from email import send_email
from ..models import Task,User

reload(sys)

# 定时任务
@celery.task()
def TimedTask():
    pass
    task = Task.query.filter(Task.del_status == 0).filter(Task.priority=='高').filter(Task.task_status != '已完成')
    for t in task:
        user = User.query.filter(User.username == t.duty)
        for u in user:
            subject = '''任务编号: %s，任务名:%s，需要你解决！''' %(t.id,t.task_name)
            content = '''任务编号: %s  <br/>任务名:%s <br/> 任务内容: %s <br/> 任务优先级：%s <br/> 任务状态:%s<br/>任务结束时间:%s ''' %(t.id,t.task_name,t.text,t.priority,t.task_status,t.end_time)
            print ('邮箱: %s ,任务主题: %s,任务内容:%s' )  % (u.email, subject, content)
            send_email(u.email,subject,content)





# 添加/修改任务 发邮件
@celery.task(name='task_mail')
def task_mail(to, subject, content):
    print u'启动异部'
    send_email(to, subject, content)
    print u'邮件发送完成'