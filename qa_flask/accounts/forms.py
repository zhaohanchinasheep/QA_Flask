import hashlib

from flask import request
from flask_login import login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
# 昵称长度验证用length,验证两次密码输入是否一致用EqualTo
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

import utils
from models import User, db, UserProfile, LoginHistory
from utils import constants
from utils.validators import phone_required


class RegisterForm(FlaskForm):
    username = StringField(label='用户名', render_kw={'class': 'form-control input-lg',
                                                   'placeholder': '请输入用户名'},
                           validators=[DataRequired('请输入用户名'), phone_required])
    nickname = StringField(label='用户昵称', render_kw={'class': 'form-control input-lg',
                                                    'placeholder': '请输入用户昵称'},
                           validators=[DataRequired('请输入用户昵称'),
                                       Length(min=2, max=20, message='昵称长度在2-20之间')])
    password = PasswordField(label='密码', render_kw={'class': 'form-control input-lg',
                                                    'placeholder': '请输入密码'},
                             validators=[DataRequired('请输入用户密码')])
    confirm_password = PasswordField(label='确认密码', render_kw={'class': 'form-control input-lg',
                                                              'placeholder': '确认密码'},
                                     validators=[DataRequired('请再次输入密码'),
                                                 EqualTo('password', message='两次密码输入不一致')])

    def validate_username(self, field):
        """检测用户名是否已存在"""
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('该用户名已存在')
        return field

    def register(self):
        """将用户信息添加到数据表中"""
        # 1.获取表单信息
        username = self.username.data
        nickname = self.nickname.data
        password = self.password.data
        # 2.添加到db.session
        try:
            # 加密存储密码
            password = hashlib.sha256(password.encode()).hexdigest()
            user_obj = User(username=username, nickname=nickname, password=password)
            db.session.add(user_obj)
            profile = UserProfile(username=username, user=user_obj)
            db.session.add(profile)
            db.session.commit()
            # 3.若注册成功，返回user_obj
            return user_obj
        except Exception as e:
            print(e)


class LoginForm(FlaskForm):
    username = StringField(label='用户名', render_kw={'class': 'form-control input-lg',
                                                   'placeholder': '请输入用户名'},
                           validators=[DataRequired('请输入用户名'), phone_required])
    password = PasswordField(label='密码', render_kw={'class': 'form-control input-lg',
                                                    'placeholder': '请输入密码'},
                             validators=[DataRequired('请输入用户密码')])

    # 重写validate函数
    def validate(self):
        # 先调用父类的validate函数，处理上面的validators属性
        result = super().validate()
        # 取到用户输入的值
        username = self.username.data
        password = self.password.data
        # 验证加密后的密码是否一致
        # password = hashlib.sha256(password.encode()).hexdigest()
        if result:
            user = User.query.filter_by(username=username,password = password).first()
            # 验证不成功
            if user is None:
                result = False
                self.username.errors = ['用户名或密码错误']
            # 验证成功但用户名被禁用
            elif user.status == constants.UserStatus.USER_IN_ACTIVE.value:
                result = False
                self.username.errors = ['该用户已被禁用']
        return result

    def dologin(self):
        """登陆后，将登陆信息保存在数据库"""
        # 1.获取用户信息
        username = self.username.data
        password = self.password.data
        try:
            # 2.查找对应用户
            # TODO:验证加密后的密码是否正确
            # password = hashlib.sha256(password.encode()).hexdigest()
            user = User.query.filter_by(username=username, password=password).first()
            # 3.登陆用户，根据sessions，用户会话的基本原理
            # 将user.id保存在session会话中，后面使用钩子函数在跳转每一个页面时，都带上此用户id（最好写在配置函数中）
            # session['user_id'] = user.id
            login_user(user)
            # 4.记录日志
            # 获取客户端ip
            ip = request.remote_addr
            # 获取客户端设备，在请求头中
            ua = request.headers.get('user-agent', None)
            obj = LoginHistory(username=username, ip=ip, ua=ua, user=user)
            db.session.add(obj)
            db.session.commit()
            return user
        except Exception as e:
            print(e)
            return None


