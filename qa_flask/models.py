#!/usr/bin/env python3
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from utils import constants
import pymysql
pymysql.install_as_MySQLdb()



db = SQLAlchemy()

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
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class UserProfile(db.Model):
    """用户详细信息表"""
    __tablename__ = "accounts_user_profile"
    id = db.Column(db.Integer, primary_key=True)
    # 真实姓名
    real_name = db.Column(db.String(64))
    sex = db.Column(db.String(16))
    # 用户格言
    maxim = db.Column(db.String(128))
    # 用户地址
    address = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 建立外键关联
    # 用户id，关联user表
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 用户姓名，关联user表
    username = db.Column(db.String(64))
    # 建立反向引用
    user = db.relationship("User", backref=db.backref('profile',uselist = False))


class LoginHistory(db.Model):
    """用户登陆历史表"""
    __tablename__ = "accounts_login_history"
    id = db.Column(db.Integer, primary_key=True)
    # user_id 与user表建立外键关联
    user_id = db.Column(db.Integer,db.ForeignKey('accounts_user.id'))
    # username 与user 表建立外键关联
    username = db.Column(db.String(64),nullable = False)
    # 账号平台
    login_type = db.Column(db.String(32))
    # IP地址
    ip = db.Column(db.String(32))
    # 登陆来源
    ua = db.Column(db.String(128))
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    #  建立反向引用
    user = db.relationship('User',backref = db.backref('history_list',lazy='dynamic'))


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
    is_valid = db.Column(db.Boolean, default = True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 反向引用
    user = db.relationship('User',backref = db.backref('third',uselist = False))


class Question(db.Model):
    """问题表"""
    __tablename__='qa_question'
    id = db.Column(db.Integer, primary_key=True)
    # user_id 与user表建立外键关联
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 标题
    title = db.Column(db.String(128),nullable = False)
    # 描述
    desc = db.Column(db.String(256))
    # 图片地址
    img = db.Column(db.String(256))
    # 问题内容
    content = db.Column(db.Text,nullable = False)
    # 排序
    reorder = db.Column(db.Integer,default = 0)
    is_valid = db.Column(db.Boolean,default = True)
    # 浏览次数
    view_count  = db.Column(db.Integer,default = 0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 反向引用
    user = db.relationship('User',backref = db.backref('question_list',lazy = 'dynamic'))

    @property
    def follow_count(self):
        """关注的数量"""
        return self.question_follow_list.filter_by(is_valid = True).count()



class Answer(db.Model):
    """回答表"""
    __tablename__ = 'qa_answer'
    id = db.Column(db.Integer, primary_key=True)
    # user_id 与user表建立外键关联
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer,db.ForeignKey('qa_question.id'))
    content = db.Column(db.Text,nullable = False)
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 反向引用
    user = db.relationship('User', backref=db.backref('answer_list',lazy='dynamic'))
    question = db.relationship('Question', backref=db.backref('answer_list', lazy='dynamic'))
    # 评论数量
    ### 在这个类中定义了的数据，不管有没有存入数据库，都可以在html中调用
    @property
    def comment_count(self):
        return self.question_comment_list.filter_by(is_valid = True).count()

class AnswerComment(db.Model):
    """评论"""
    __tablename__ = 'qa_answer_comment'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    # 关联评论
    replay_id = db.Column(db.Integer, db.ForeignKey('qa_answer_comment.id'))
    # 关联问题
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 关联回答
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    # 评论内容
    content = db.Column(db.String(512), nullable=False)
    # 点赞人数
    love_count = db.Column(db.Integer,default = 0)
    is_valid = db.Column(db.Boolean, default=True)
    # 是否公开
    is_public = db.Column(db.Boolean,default = True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 反向引用
    user = db.relationship('User', backref=db.backref('answer_comment_list',lazy='dynamic'))
    question = db.relationship('Question', backref=db.backref('question_comment_list',lazy='dynamic'))
    answer = db.relationship('Answer', backref=db.backref('answer_comment_list',lazy='dynamic'))


class AnswerLove(db.Model):
    """回答点赞"""
    __tablename__ = 'qa_answer_love'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_love_list', lazy='dynamic'))
    # 建立与答案的一对多属性
    answer = db.relationship('Answer', backref=db.backref('answer_love_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_love_list', lazy='dynamic'))


class AnswerCollect(db.Model):
    __tablename__ ='qa_answer_collect'
    """我收藏的回答"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    answer_id = db.Column(db.Integer, db.ForeignKey('qa_answer.id'))
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('answer_collect_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_collect_list', lazy='dynamic'))
    # 建立与答案的一对多属性
    answer = db.relationship('Answer', backref=db.backref('answer_collect_list', lazy='dynamic'))


class QuestionFollow(db.Model):
    """我关注的问题"""
    __tablename__ = 'qa_question_follow'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('accounts_user.id'))
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    is_valid = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    # 建立与用户的一对多属性
    user = db.relationship('User', backref=db.backref('question_follow_list', lazy='dynamic'))
    # 建立与问题的一对多属性
    question = db.relationship('Question', backref=db.backref('question_follow_list', lazy='dynamic'))


class QuestionTags(db.Model):
    """问题标签"""
    __tablename__ = "qa_question_tags"
    id = db.Column(db.Integer, primary_key=True)
    q_id = db.Column(db.Integer, db.ForeignKey('qa_question.id'))
    # 标签名称
    tag_name = db.Column(db.String(16),nullable = False)
    is_valid = db.Column(db.Boolean, default= True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    question = db.relationship('Question', backref=db.backref('tag_list', lazy = 'dynamic'))
