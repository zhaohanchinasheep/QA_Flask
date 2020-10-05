#!/usr/bin/env python3
from flask import Flask
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





if __name__ == '__main__':
    app.run()
