# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from datetime import datetime
import sys
from flask import render_template,request,flash,redirect,url_for, current_app, jsonify,session
from flask_login import login_required, current_user
from . import main
from .forms import Addtask,SearchTask,TaskContent,EditTask
from ..models import User, Task,TaskTxt,Project,Department,Role
from app import db
from app.tasks.printy import task_mail
from hashlib import md5
from ..decorators import permission_required
from config import Config
import os
from werkzeug.utils import secure_filename

reload(sys)
sys.setdefaultencoding('utf8')

@main.route('/',methods=['GET', 'POST'])
def i():
    return redirect(url_for('auth.login'))


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
        #获取分页数
        page = request.args.get('page',1,type=int)
        #分页
        per_page = current_app.config['POSTS_PER_PAGE']
        pagination = Task.query.filter(Task.del_status == 0).order_by(db.desc(Task.id)).paginate(page,per_page=per_page,error_out=False)
        task = pagination.items


        search_form = SearchTask()
        if search_form.validate_on_submit():
            _search_form = search_form.search_task.data
            _search_task = Task.query.filter(Task.del_status == 0).filter(Task.task_name.ilike('%'+ _search_form + '%'))
            return render_template('index.html',tasks=_search_task,search_form=search_form,pagination=pagination)
        else:
            return render_template('index.html',tasks=task,search_form=search_form,pagination=pagination)



@main.route('/user/')
@login_required
@permission_required(1)
def user():
    #取出所有用户数据
    user = User.query.filter_by().all()
    dep = Department.query.filter_by().all()
    role = Role.query.filter_by().all()
    return render_template('user/user.html',users=user,deps=dep,roles=role)



@main.route('/add_user/',methods=['POST'])
@login_required
@permission_required(2)
def add_user():
    # 检查是否为ajax请求
    if request.method == 'POST':
        username = request.form.get('username', u'无用户名')
        pwd = request.form.get('password', u'无密码')
        email = request.form.get('email', u'无邮箱')
        sex = request.form.get('sex','')
        role_id = request.form.get('role_id','')
        tel = request.form.get('tel','')
        qq = request.form.get('qq','')
        department = request.form.get('department','')

        if email and pwd:
            _user = User(username=username, password=md5(pwd).hexdigest(), email=email, sex=sex, role_id=role_id,
                         tel=tel, qq=qq, department=department, date=datetime.now())
            db.session.add(_user)
            flash('添加用户成功！', 'success')
            return ("success");
        else:
            return '数据不合法！'
    else:
        return '请求不合法！'


@main.route('/edit_user/',methods=['POST','GET'])
@login_required
@permission_required(4)
def edit_user():
    # 禁用用户
    if request.method == 'GET':
        uid = request.args.get('user_id')
        ustatus = int(request.args.get('user_op'))

        #  ustatus 1 表示禁用，0 表示启动
        if ustatus == 1:
            u = User.query.filter(User.id==uid).first()
            u.status = 1
            db.session.commit()
            return jsonify("'msg':'禁用成功'")
        else:
            u = User.query.filter(User.id==uid).first()
            u.status = 0
            db.session.commit()
            return jsonify("'msg':'启用成功'")
    return 'ok!'

@main.route('/checkemail/',)
@login_required
def checkemail():
        email = User.query.filter_by(email=request.args.get('email','').lower()).first()
        return jsonify(email is None)


@main.route('/role')
@login_required
def role():
    #username = User.query.filter_by().all()
    #pw = User.query.filter_by(text=form.password.data).first()


    # 取出所有角色
    roles = Role.query.filter_by().all()

    return render_template('user/role.html',roles=roles)


@main.route('/add_task',methods=['GET', 'POST'])
@login_required
@permission_required(6)
def add_task():
    form = Addtask()
    #给addtask form 下拉列表 赋初始化值
    form.duty.choices = [(duty.username, duty.username)
                         for duty in User.query.filter(User.username != 'admin').all()]  # 取出不等于admin的用户
    form.assist.choices = form.duty.choices
    form.project.choices = [(project.pro_name, project.pro_name)
                            for project in Project.query.order_by(Project.pro_name).all()]
    form.department.choices = [(department.name, department.name)
                               for department in Department.query.order_by(Department.name).all()]
    user = User.query.filter_by().all()
    project = Project.query.filter_by().all()
    _start_time = request.form.get('start_time')
    _end_time = request.form.get('end_time')
    if form.validate_on_submit():
        input_date = datetime.now()
        task_user = current_user.username
        task_name = form.task_name.data
        text = form.text.data
        task_status = '未开始'
        department = form.department.data
        if task_name:
            task = Task(task_name=task_name,duty=form.duty.data,assist=form.duty.data,project=form.project.data,
                        priority=form.priority.data,task_type=form.task_type.data,start_time=_start_time,
                        end_time=_end_time,text=text,input_date=input_date,task_user=task_user,task_status=task_status,department=department)
            db.session.add(task)
            #添加任务后，发送邮件给任务责任人
            _user = Task.query.order_by(db.desc(Task.id)).first()
            to_mail = User.query.filter(User.username==_user.duty).first()
            subject = '''新任务，任务编号: %s，任务名:%s，需要你解决！''' %(_user.id,_user.task_name)
            content = '''任务编号: %s  <br/>任务名:%s <br/> 任务内容: %s <br/>任务结束时间:%s<br/>优先级:%s ''' \
                      %(_user.id,_user.task_name,_user.text,_user.end_time,_user.priority)
            task_mail(to_mail.email,subject,content)
            flash('添加成功.')
            return redirect(url_for('main.index'))
        else:
            flash('数据输入有错，请重新输入！！！！！！！！！！！')

    return render_template('add_task.html',form=form,users=user,projects=project)


#删除任务
@main.route('/del_task/<int:task_id>')
@permission_required(7)
@login_required
def del_task(task_id):
    if task_id:
        result = Task.query.filter(Task.id == task_id).first()
        if result.task_status == '未开始':
            result.del_status = 1
            db.session.commit()
        else:
            return '进行中/完成任务不能删除！'
    else:
        flash('非法删除.')

    return redirect(url_for('main.index'))

#搜索任务
@main.route('/search_task/<status>',methods=['GET'])
@login_required
def search_task(status):
    search_form = SearchTask()
    #获取分页数
    page = request.args.get('page',1,type=int)
    per_page = current_app.config['POSTS_PER_PAGE']

    if status == 'no_start':
        #分页
        pagination = Task.query.filter(Task.task_status=="未开始").paginate(page,per_page=per_page,error_out=False)
        _search_task = pagination.items
        return render_template('index.html',tasks=_search_task,search_form=search_form,pagination=pagination)
    elif status == 'start':
        pagination = Task.query.filter(Task.task_status=="进行中").paginate(page,per_page=per_page,error_out=False)
        _search_task = pagination.items
        return render_template('index.html',tasks=_search_task,search_form=search_form,pagination=pagination)
    elif status == 'end_start':
        pagination = Task.query.filter(Task.task_status=="已完成").paginate(page,per_page=per_page,error_out=False)
        _search_task = pagination.items
        return render_template('index.html',tasks=_search_task,search_form=search_form,pagination=pagination)
    else:
        return redirect(url_for('main.index'))

#修改任务
@main.route('/edit_task/<int:task_id>', methods=['POST','GET'])
@login_required
@permission_required(8)
def edit_task(task_id):
    form = EditTask()
    #给addtask form 下拉列表 赋初始化值
    form.duty.choices = [(duty.username, duty.username)
                         for duty in User.query.filter(User.username != 'admin').all()]  # 取出不等于admin的用户
    form.assist.choices = form.duty.choices
    form.project.choices = [(project.pro_name, project.pro_name)
                            for project in Project.query.order_by(Project.pro_name).all()]
    form.department.choices = [(department.name, department.name)
                               for department in Department.query.order_by(Department.name).all()]
    _edit = Task.query.filter(Task.id==task_id).first()
    _edit_id = task_id
    _task_name = request.form.get('task_name')
    _duty = request.form.get('duty')
    _assist = request.form.get('assist')
    _project = request.form.get('project')
    _priority = request.form.get('priority')
    _task_type = request.form.get('task_type')
    _department = request.form.get('department')
    _progres = request.form.get('progress')  #获取任务进度
    _text = request.form.get('text')
    _end_date = datetime.now()   #进度完成写入提交时间
    _submit = request.form.get('submit')

    if _edit:
        if _edit.duty == current_user.username or _edit.task_user == current_user.username or \
                        _edit.assist == current_user.username or current_user.id == 1:


            if _edit.task_status == '已完成':
                return "已完成的任务禁止修改！！！！"

            if _submit == '修改':
                #获取修改任务进度状态
                if _progres == '已完成':
                    #已完成修改完成时间
                    _update = {"task_name":_task_name,"duty":_duty,"assist":_assist,"project":_project,"task_type":_task_type,
                               "end_time":_end_date,"text":_text,"task_status":_progres,"department":_department,"priority":_priority}
                else:
                    _update = {"task_name":_task_name,"duty":_duty,"assist":_assist,"project":_project,"task_type":_task_type,
                               "task_status":_progres,"text":_text,"department":_department,"priority":_priority}

                if Task.query.filter(Task.id==task_id).update(_update):
                    #修改任务后，发送邮件给任务责任人
                    to_mail = User.query.filter(User.username==_edit.duty).first()
                    subject = '''任务编号: %s，任务名:%s 有变更！"''' %(_edit_id,_task_name)
                    content = '''任务编号: %s  <br/>任务名:%s <br/> 任务内容: %s <br/>任务结束时间:%s <br/>任务状态:%s<br/>优先级:%s''' \
                              %(_edit_id,_task_name,_text,_end_date,_progres,_priority)
                    task_mail.delay(to_mail.email,subject,content)

                return redirect(url_for('main.index'))

            return render_template('edit_task.html',edit_task=_edit,form=form)
        else:
            return "任务相关人员可以修改，请于管理员联系！！！！！！"
    else:
        return "非法请求"



#任务详情
@main.route('/task/<int:task_id>', methods=['POST','GET'])
@login_required
def task(task_id):
    task_con = TaskContent()
    if task_con.validate_on_submit():
        _date = datetime.now()
        txt = task_con.text.data
        task_user = current_user.username
        _task = TaskTxt(id_task=task_id,user_name=task_user,txt=txt,date=_date)
        db.session.add(_task)
        flash('添加成功.')

    else:
        if task_id:
            task = Task.query.get_or_404(task_id)
            #获取任务对应的回复数据
            task_txt = TaskTxt.query.filter(TaskTxt.id_task==task_id)
            avatars = User.query.filter()
            return render_template('task_content.html',task_content=task,task_txts=task_txt,task_con=task_con,avatars=avatars)

    return redirect(url_for('main.task',task_id=task_id))



# 我的资料
@main.route('/my_info',methods=['POST','GET'])
@login_required
def my_info():
    if request.method == 'POST':
        new_pass = md5(request.form.get('password')).hexdigest()
        result = User.query.filter(User.id == current_user.id).first()
        result.password = new_pass
        db.session.commit()
        return redirect(url_for('auth.logout'))
    else:

        return render_template('user/my_info.html')

# 上传头像
@main.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        files = request.files['file']
        myhash = md5()
        f = file(os.path.join(Config.UPLOAD_FOLDER, files.filename), 'rb')
        while True:
            b = f.read(8096)
            if not b:
                break
            myhash.update(b)
        f.close()
        if '.' in files.filename and files.filename.rsplit('.', 1)[1] in Config.ALLOWED_EXTENSIONS:
            # 上传文件
            # 保存文件
            filename = secure_filename(files.filename)
            files.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            u = User.query.filter(User.id == current_user.id).first()
            u.avatar = filename
            db.session.commit
            img = {'state': 1}
            return jsonify(img)
        else:
            img = {'state': 0}
            return jsonify(img)
    else:
        return '不允许访问！！！！'