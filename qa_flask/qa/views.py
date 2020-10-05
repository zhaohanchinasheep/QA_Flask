#!/usr/bin/env python3


from flask import Blueprint, render_template, request, abort

from models import Question

qa = Blueprint('qa',__name__,template_folder="templates",static_folder = "..assets")

@qa.route('/index')
def index():
    """ 首页 """
    return render_template('index.html')




@qa.route('/detail/<int:q_id>')
def detail(q_id):
    """ 文章详情页面 """
    # 1.搜索出来的是一条问题的信息
    question = Question.query.get(q_id)
    # 当问题被逻辑删除时
    if not question.is_valid:
       abort(404)
    # 2.展示第一条回答的信息
    answer = question.answer_list.filter_by(is_valid = True).first()
    return render_template('detail.html',question = question,answer = answer)


@qa.route('/follow')
def follow():
    """ 关注页面 """
    # 用分页的方式显示qa_question中的所有有效数据
    per_page = 20
    # 获取get请求参数,默认为1
    page = int(request.args.get('page',1))
    page_data = Question.query.filter_by(is_valid = True).paginate(page=page,per_page = per_page)
    return render_template('follow.html',page_data = page_data)


@qa.route('/write')
def write():
    """ 写文章页面 """
    return render_template('write.html')

