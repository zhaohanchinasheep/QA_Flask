import hashlib

from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user

from accounts.forms import RegisterForm, LoginForm


# step2 实例化蓝图对象
from models import User, LoginHistory, db

accounts = Blueprint('accounts',__name__,template_folder = "templates",
                     static_folder='../assets')


@accounts.route('/login',methods=['GET','POST'])
def login():
    """ 登陆页面 """
    form = LoginForm()
    next_url = request.values.get('next', url_for('qa.index'))
    if form.validate_on_submit():
        user = form.dologin()
        if user:
            # 5.跳转到首页
            # 使用flask-login扩展 next 存储的是
            flash('{}，欢迎回来'.format(user.nickname),'success')
            return redirect(next_url)
        else:
            flash('登陆失败，请稍后重试','danger')
    return render_template('login.html',next_url=next_url,form = form)


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

@accounts.route('/logout')
def logout():
    logout_user()
    flash("欢迎下次再来",'success')
    return redirect(url_for('accounts.login'))


@accounts.route('/mine')
def mine():
    """ 个人中心 """
    return render_template('mine.html')
