#!/usr/bin/env python3
from flask import Flask, session, g
from models import db, User
from accounts.views import accounts
from qa.views import qa
from utils.filters import number_split, dt_format_show
from flask_login import LoginManager
from flask_ckeditor import CKEditor # 富文本编辑器

app = Flask(__name__, static_folder="assets")
# 从配置文件加载配置
app.config.from_object('conf.Config')

# 数据库初始化
db.init_app(app)

# 富文本扩展初始化
ckeditor = CKEditor()
ckeditor.init_app(app)

# 登陆验证
login_manager = LoginManager()
# 设置点击某一个页面后跳转的地址，即点击write页面先跳转到登陆页面
login_manager.login_view = 'accounts.login'
login_manager.login_message = '请登陆'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)

# step3 注册蓝图
app.register_blueprint(accounts,url_prefix='/accounts')
app.register_blueprint(qa,url_prefix='/')

# 注册过滤器
app.jinja_env.filters['number_split'] = number_split
app.jinja_env.filters['dt_format_show'] = dt_format_show
# flask-login的扩展，使用回调


@login_manager.user_loader
def load_user(user_id):
    """表示从存储在会话中的user_id中重新加载User"""
    return User.query.get(user_id)

# # 设置钩子函数，装饰器函数
# # 重点，使用g对象
# @app.before_request
# def before_request():
#     """如果有用户id，设置到全局对象g"""
#     user_id = session.get('user_id',None)
#     # 将用户id保存到g对象中
#     g.current_user = user_id






if __name__ == '__main__':
    app.run()
