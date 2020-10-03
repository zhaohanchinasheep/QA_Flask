from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

import constants

app = Flask(__name__, static_folder="assets")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Admin@123456@localhost/qa_flask'
db = SQLAlchemy(app)


class User(db.Model):
    """用户表模型建立"""
    __tablename__ = "accounts_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    # 用户昵称
    nickname = db.Column(db.String(64))
    password = db.Column(db.String(256), nullable=False)
    # 头像文件地址
    avatar = db.Column(db.String(256))
    # 用户账户状态
    status = db.Column(db.SmallInteger, default=constants.UserStatus.USER_ACTIVE.value)
    # 是否为超级管理员，超级管理员可以对所有内容进行管理
    is_super = db.Column(db.SmallInteger, default=constants.UserRole.COMMON.value)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Colunm(db.DateTime, default=datetime.now, onupdate=datetime.now)


class UserProfile(db.Model):
    """用户详细信息表"""
    __tablename__ = "accounts_user_profile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 真实姓名
    real_name = db.Column(db.String(64))
    sex = db.Column(db.String(1))
    # 用户格言
    maxim = db.Column(db.String(256))
    # 用户地址
    address = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 建立外键关联
    # 用户id，关联user表
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 用户姓名，关联user表
    username = db.Column(db.String(64), db.ForeignKey('accounts_user.username'))
    # 建立反向引用
    user = db.relationship("User", backref=db.backref('profile'),uselist = False)


class LoginHistory(db.Model):
    """用户登陆历史表"""
    __tablename__ = "accounts_login_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id 与user表建立外键关联
    user_id = db.Column(db.Integer,db.ForeignKey('accounts_user.id'))
    # username 与user 表建立外键关联
    username = db.Colunm(db.String(64),db.ForeignKey('account_user.username'))
    # 账号平台
    login_type = db.Colunm(db.String(64),nullable = False)
    # IP地址
    ip  = db.Column(db.String(128))
    # 登陆来源
    ua = db.Column(db.String(128))
    #  建立反向引用
    user = db.relationship('User',backref = db.backref('login_history'),uselist=False)


class Third(db.Model):
    """第三方登陆信息"""
    __tablename__="account_third"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id 与user表建立外键关联
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 平台类型
    types = db.Column(db.String(64),nullable = False)
    # 登陆名
    login_name = db.Column(db.String(64),nullable=False)
    is_valid = db.Column(db.String(1),default = constants.Valid.IS_VALID.value)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 反向引用
    user = db.relationship('User',back_ref = db.backref('third'),uselist = False)

class QaQuestion(db.Model):
    """问题表"""
    __tablename__='qa_question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id 与user表建立外键关联
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 标题
    title = db.Column(db.String(128),nullable = False)
    # 描述
    desc = db.Column(db.String(32))
    # 图片地址
    img = db.Column(db.String(32))
    # 问题内容
    content = db.Column(db.String(3072),nullable = False)
    # 排序
    reorder = db.Column(db.Integer,default = 1)
    is_valid = db.Column(db.String(1),default = constants.Valid.IS_VALID.value)
    # 浏览次数
    view_count  = db.Column(db.Integer,default = 0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 反向引用
    user = db.relationship('User',back_ref = db.backref('question'),uselist = False)


class QaAnswer(db.Model):
    """回答表"""
    __tablename__ = 'qa_answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id 与user表建立外键关联
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer,db.ForeignKey('qa_question.id'))
    content = db.Column(db.String(1024),nullable = False)
    is_valid = db.Column(db.String(1), default=constants.Valid.IS_VALID.value)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 反向引用
    user = db.relationship('User', back_ref=db.backref('answer'), uselist=False)
    question = db.relationship('QaQuestion', back_ref=db.backref('answer'), uselist=False)


class QaComment(db.Model):
    """评论"""
    __tablename__ = 'qa_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # # 关联回答
    # replay_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 关联回答
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    # 评论内容
    content = db.Column(db.String(1024), nullable=False)
    # 点赞人数
    love_count = db.Column(db.Integer,nullable = False,default = 0)
    is_valid = db.Column(db.String(1), default=constants.Valid.IS_VALID.value,nullable = False)
    # 是否公开
    is_public = db.Column(db.String(1),defaule = constants.QaPublic.IS_PUBLIC.value)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 反向引用
    user = db.relationship('User', back_ref=db.backref('comment'), uselist=False)
    question = db.relationship('QaQuestion', back_ref=db.backref('comment'), uselist=False)
    answer = db.relationship('QaAnswer', back_ref=db.backref('comment'), uselist=False)
    """
    replay_id INT NOT NULL   COMMENT '关联评论' ,
    """

class QaAnswerLove(db.Model):
    """回答点赞"""
    __tablename__ = 'qa_answer_love'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    created_at = db.Column(db.DateTime, default=datetime.now,nullable = False)
    user = db.relationship('User', back_ref=db.backref('answerlove'), uselist=False)
    question = db.relationship('QaQuestion', back_ref=db.backref('answerlove'), uselist=False)
    answer = db.relationship('QaAnswer', back_ref=db.backref('answerlove'), uselist=False)


class QaAnswerCollect(db.Model):
    __tablename__ ='qa_answer_collect'
    """我收藏的回答"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    is_valid = db.Column(db.String(1), default=constants.Valid.IS_VALID.value, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user = db.relationship('User', back_ref=db.backref('collect'), uselist=False)
    question = db.relationship('QaQuestion', back_ref=db.backref('collect'), uselist=False)
    answer = db.relationship('QaAnswer', back_ref=db.backref('collect'), uselist=False)


class QaQuestionFollow(db.Model):
    """我关注的问题"""
    __tablename__ = 'qa_question_follow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    is_valid = db.Column(db.String(1), default=constants.Valid.IS_VALID.value, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    user = db.relationship('User', back_ref=db.backref('follow'), uselist=False)
    question = db.relationship('QaQuestion', back_ref=db.backref('follow'), uselist=False)


class QaQuestionTags(db.Model):
    """问题标签"""
    __tablename__ = "qa_question_tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 标签名称
    tag_name = db.Column(db.String(32),nullable = False)
    is_valid = db.Column(db.String(1), default=constants.Valid.IS_VALID.value, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    question = db.relationship('QaQuestion', back_ref=db.backref('follow'), uselist=False)

@app.route('/index')
def index():
    """ 首页 """
    return render_template('index.html')


@app.route('/login')
def login():
    """ 登陆页面 """
    return render_template('login.html')


@app.route('/register')
def register():
    """ 注册页面 """
    return render_template('register.html')


@app.route('/detail')
def detail():
    """ 文章详情页面 """
    return render_template('detail.html')


@app.route('/follow')
def follow():
    """ 关注页面 """
    return render_template('follow.html')


@app.route('/mine')
def mine():
    """ 个人中心 """
    return render_template('mine.html')


@app.route('/write')
def write():
    """ 写文章页面 """
    return render_template('write.html')


if __name__ == '__main__':
    app.run()
