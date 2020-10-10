#!/usr/bin/env python3
from flask import Blueprint, render_template, request, abort, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user

from models import Question, Answer, AnswerComment, db
from qa.forms import WriteQuestionForm, WriteAnswerForm

qa = Blueprint('qa', __name__, template_folder="templates", static_folder="..assets")


@qa.route('/index')
def index():
    """ 首页 回答列表"""
    # 用分页的方式显示qa_question中的所有有效数据
    per_page = 20
    # 获取get请求参数,默认为1
    page = int(request.args.get('page', 1))
    page_data = Answer.query.filter_by(is_valid=True).paginate(page=page, per_page=per_page)
    return render_template('index.html', page_data=page_data)


@qa.route('/detail/<int:q_id>', methods=['POST', 'GET'])
def detail(q_id):
    """ 文章详情页面 """
    # 1.搜索出来的是一条问题的信息
    question = Question.query.get(q_id)
    # 当问题被逻辑删除时
    if not question.is_valid:
        abort(404)
    # 2.展示第一条回答的信息
    answer = question.answer_list.filter_by(is_valid=True).first()
    # 3.添加回答
    form = WriteAnswerForm()
    if form.validate_on_submit():
        try:
            if not current_user.is_authenticated:
                flash('请先登陆', 'danger')
                return redirect(url_for('accounts.login'))
            form.save(question=question)
            flash('回答问题成功', 'success')
            return redirect(url_for('qa.detail', q_id=q_id))
        except Exception as e:
            print(e)
    return render_template('detail.html', question=question, answer=answer, form=form)


@qa.route('comments/<int:answer_id>', methods=['GET', 'POST'])
def comments(answer_id):
    """评论"""
    answer = Answer.query.get(answer_id)
    if request.method == 'POST':
        try:
            if not current_user.is_authenticated:
                result = {'code': '1', 'message': '请先登陆'}
                # 对象以json格式返回
                return jsonify(result), 400
            # 1.获取数据
            # content,question等都是请求的对象，并不是值
            # content是异步请求中的content值
            # 获取表单数据或者传递的参数，content要么为表单的name属性，要么是异步请求中传递过来的data中的参数
            content = request.form.get('content', '')
            reply_id = request.form.get('reply_id', None)
            print(reply_id)
            question = answer.question
            comment_obj = AnswerComment(content=content,
                                        user=current_user,
                                        question=question,
                                        answer=answer,
                                        reply_id=reply_id)

            db.session.add(comment_obj)
            db.session.commit()
            return '', 201
        except Exception as e:
            print(e)
            result = {'code': '1', 'message': '服务器正忙，请稍后重试'}
            return jsonify(result), 400
    else:
        # 获取评论列表（没有发表评论时的操作）
        try:
            page = int(request.args.get('page', 1))
            page_data = answer.comment_list().paginate(page=page, per_page=3)
            print(page)
            # data表示的是每一页的评论数据
            data = render_template('comments.html', page_data=page_data,answer=answer)
            return jsonify({'code':0,'data':data,'meta':{'page':page}}),200
        except Exception as e:
            print(e)
            return jsonify({'code': 1, 'data': '', 'message':'服务器正忙，请稍后再试'}), 500

@qa.route('/comment/love/<int:comment_id>',methods=['POST'])
def comment_love(comment_id):
    """为评论点赞"""
    try:
        if not current_user.is_authenticated:
            return '',401
        # 处理数据库中的点赞数量
        comment_obj=AnswerComment.query.get(comment_id)
        comment_obj.love_count +=1
        db.session.add(comment_obj)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)
    return '',201



@qa.route('/follow')
def follow():
    """ 关注页面 """
    # 用分页的方式显示qa_question中的所有有效数据
    per_page = 20
    # 获取get请求参数,默认为1
    page = int(request.args.get('page', 1))
    page_data = Question.query.filter_by(is_valid=True).paginate(page=page, per_page=per_page)
    return render_template('follow.html', page_data=page_data)


@qa.route('/qa/list')
def question_list():
    try:
        # 用分页的方式显示qa_question中的所有有效数据
        per_page = 2
        # 获取get请求参数,默认为1
        page = int(request.args.get('page', 1))
        page_data = Question.query.filter_by(is_valid=True).paginate(page=page, per_page=per_page)
        data = render_template('qa_list.html', page_data=page_data)
        return {'code': 0, 'data': data}
    except Exception as e:
        print(e)
        data = ''
    return {'code': 1, 'data': data}


# login_require 是flask-login扩展的内置装饰器,未进行某验证(比如：登陆)点击此页面就会调转到login_manager.login_view指定的页面
@qa.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    """ 写文章页面 """
    form = WriteQuestionForm()
    # 实现表单提交逻辑
    if form.validate_on_submit():
        try:
            que_obj = form.save()

            if que_obj:
                flash('问题发布成功', 'success')
                return redirect(url_for('qa.index'))
        except Exception as e:
            print(e)
        #   flash不能写在else里面，否则每post一次，都要进行flash展示
        flash('问题发布失败，请稍后重试', 'danger')
    return render_template('write.html', form=form)
