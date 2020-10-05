import hashlib

from flask import Blueprint, render_template, flash, redirect, url_for, session, request

from accounts.forms import RegisterForm, LoginForm

# step2 实例化蓝图对象
from models import User, LoginHistory, db

accounts = Blueprint('accounts',__name__,template_folder = "templates",
                     static_folder='../assets')


@accounts.route('/login',methods=['GET','POST'])
def login():
    """ 登陆页面 """
    form = LoginForm()
    if form.validate_on_submit():
        # 1.获取用户信息
        username = form.username.data
        password = form.password.data
        # 2.查找对应用户
        # TODO:验证加密后的密码是否正确
        # password = hashlib.sha256(password.encode()).hexdigest()
        user = User.query.filter_by(username=username, password=password).first()
        # 3.登陆用户，根据sessions，用户会话的基本原理
        # 将user.id保存在session会话中，后面使用钩子函数在跳转每一个页面时，都带上此用户id（最好写在配置函数中）
        session['user_id'] = user.id
        # 4.记录日志
        # 获取客户端ip
        ip = request.remote_addr
        # 获取客户端设备，在请求头中
        ua = request.headers.get('user-agent',None)
        obj = LoginHistory(username = username,ip = ip ,ua = ua, user = user)
        db.session.add(obj)
        db.session.commit()
        # 5.跳转到首页
        flash('{}，欢迎回来'.format(user.nickname),'success')
        return redirect(url_for('qa.index'))
    else:
        print(form.errors)
    return render_template('login.html',form = form)


@accounts.route('/register',methods = ['GET','POST'])
def register():
    """ 注册页面 """
    form = RegisterForm()
    if form.validate_on_submit():
        user_obj = form.register()
        if user_obj:
            # flash和模版深度绑定，需要在视图函数中完成
            flash('注册成功，请登陆','success')
            # 注册成功，跳转到登陆页面
            return redirect(url_for('accounts.login'))
        else:
            # danger是bootstrap中的css
            flash('注册失败，请稍后再试','danger')
    return render_template('register.html',form = form)


@accounts.route('/mine')
def mine():
    """ 个人中心 """
    return render_template('mine.html')
