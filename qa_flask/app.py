#!/usr/bin/env python3
from flask import Flask, session, g
from models import db
from accounts.views import accounts
from qa.views import qa
from utils.filters import number_split

app = Flask(__name__, static_folder="assets")
# 从配置文件加载配置
app.config.from_object('conf.Config')
# 数据库初始化
db.init_app(app)
# step3 注册蓝图
app.register_blueprint(accounts,url_prefix='/accounts')
app.register_blueprint(qa,url_prefix='/')

# 注册过滤器
app.jinja_env.filters['number_split'] = number_split

# 设置钩子函数，装饰器函数
# 重点，使用g对象
@app.before_request
def before_request():
    """如果有用户id，设置到全局对象g"""
    user_id = session.get('user_id',None)
    # 将用户id保存到g对象中
    g.current_user = user_id






if __name__ == '__main__':
    app.run()
