# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from . import login_manager, db
from flask_login import UserMixin,AnonymousUserMixin
from flask import session





# 角色-节点关系表
role_node = db.Table('role_node',
                        db.Column('id',db.Integer,primary_key=True),
                        db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                        db.Column('node_id', db.Integer, db.ForeignKey('node.id'))
                        )




#用户表
class User(UserMixin,db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    date = db.Column(db.DateTime())
    sex = db.Column(db.String(64))
    department = db.Column(db.Integer, db.ForeignKey('department.id'))  # 部门外键
    qq = db.Column(db.String(64))
    email = db.Column(db.String(64))
    tel = db.Column(db.String(255))
    status = db.Column(db.Integer,default=0)      #用户状态 0:激活  1:禁用
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  #  角色外键

    def __repr__(self):
        return '<email %r>' % (self.email)

    def to_json(self):
        return dict(id=self.id,username=self.username,sex=self.sex,department=self.department,qq=self.qq,
                    email=self.email,tel=self.tel,role_id=self.role_id)

    def can(self,permissions):
        if permissions:

            #if self.role_id == 1:
            #    return True
            #判断permissions是否在session['user']['node']字典键中
            print session['user']['node']
            if session['user']['node']. has_key(permissions):
                #返回true有权限
                return True
            #返回False无权限
            return False
        return False
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False


login_manager.anonymous_user = AnonymousUser

# 角色表
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    txt = db.Column(db.String(64))
    users = db.relationship('User', backref='role')
    node_id = db.relationship('Node', secondary=role_node, backref='role_node')

    def __repr__(self):
        return '<Role %r>' % self.name




# 节点表
class Node(db.Model):
    __tablename__ ='node'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    txt = db.Column(db.String(64))

    def __repr__(self):
        return '<node %r>' % self.id



# 部门表
class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.String(255))
    #user_id = db.relationship('User',backref='department')
    users = db.relationship('User', backref='dep')


    #返回部门信息
    def __repr__(self):
        return '<dep %r>' %(self.dep)

#项目列表
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer,primary_key=True)
    pro_name = db.Column(db.String(32))
    text = db.Column(db.String(32))



    #返回项目列表
    def __repr__(self):
        return '<pro_name  %r>' %(self.pro_name)


#任务表
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer,primary_key=True)
    task_user = db.Column(db.String(32))   # 任务发起人
    input_date = db.Column(db.DateTime())   # 任务发起时间
    task_name = db.Column(db.String(255))   # 任务名
    duty = db.Column(db.String(32))        # 责任人
    assist = db.Column(db.String(32))      # 协助人
    project = db.Column(db.String(32))     # 所属项目
    department = db.Column(db.String(32))  # 所属部门
    priority = db.Column(db.String(32))    # 优先  高 中 低
    task_type = db.Column(db.String(32))   # 任务类型
    start_time = db.Column(db.DateTime())  # 开始时间
    end_time = db.Column(db.DateTime())    # 结束时间
    task_status = db.Column(db.String(32)) # 任务进度状态 1.已完成  2.未开始 3.进行中
    text = db.Column(db.String(255))        # 任务详情
    del_status = db.Column(db.Integer,default=0)      #任务状  0.正常  1.删除
    #返回任务名
    def __repr__(self):
        return '<task_name %r>' %(self.id)




#任务回复表
class TaskTxt(db.Model):
    __tablename__ = 'task_txt'
    id = db.Column(db.Integer,primary_key=True)
    id_task = db.Column(db.Integer)   #任务ID
    user_name = db.Column(db.String(32))   #回复用户
    txt = db.Column(db.String(255))  #回复内容
    date = db.Column(db.DateTime())  #回复时间

    #返回任务回复信息
    def __repr__(self):
        return '<task_txt  %r>' %(self.task_txt)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


