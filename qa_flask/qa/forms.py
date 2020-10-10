import os
import time

from flask import current_app
from flask_login import current_user
from flask_wtf import FlaskForm  # 表单
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, FileField, TextAreaField  # 标签
from wtforms.validators import DataRequired, Length  # 验证器

from flask_ckeditor import CKEditorField  # 富文本编辑器
from models import Question, db, QuestionTags, Answer


class WriteQuestionForm(FlaskForm):
    img = FileField(label="图片",
                    render_kw={'accept': '.jpeg, .jpg, .png'},
                    validators=[FileAllowed(['png', 'jpg', 'jpeg'], '请选择合适的图片类型')])
    title = StringField(label="标题",
                        render_kw={'class': 'form-control',
                                   'placeholder': '请输入标题（最多50个字）'
                                   },
                        validators=[DataRequired('请输入标题'),
                                    Length(min=5, max=50, message='标题长度为5-50个字')])
    tags = StringField(label="标签",
                       render_kw={'class': 'form-control',
                                  'placeholder': '输入标签，用,分隔'
                                  })
    desc = TextAreaField(label="描述",
                         render_kw={'class': 'form-control',
                                    'placeholder': '简述'},
                         validators=[Length(max=150, message='描述最长为150个字')])
    content = CKEditorField(label="文章内容",
                            render_kw={'class': 'form-control',
                                       'placeholder': '请输入正文'},
                            validators=[DataRequired('请输入正文'),
                                        Length(min=5, message='正文不少于5个字')])

    def save(self):
        """保存用户写的文章"""
        # 1.获取图片
        img = self.img.data
        if img:
            img_name = secure_filename(img.filename)
            now = str(int(time.time()))
            img_name = now + img_name
            img_path = os.path.join(current_app.config['MEDIA_ROOT'], img_name)
            img.save(img_path)
        # 2.保存文章内容
        title = self.title.data
        desc = self.desc.data
        content = self.content.data
        # user可以直接使用flask-login中的current_user
        que_obj = Question(img=img_name, title=title, desc=desc, content=content,
                           user=current_user)
        db.session.add(que_obj)
        # 3.保存标签
        tags = self.tags.data
        for tag in tags.split('，'):
            if tag:
                tag_obj = QuestionTags(tag_name=tag, question=que_obj)
                db.session.add(tag_obj)
        db.session.commit()
        return que_obj


class WriteAnswerForm(FlaskForm):
    """保存用户写的文章回答"""
    content = CKEditorField(label='回答内容',
                            render_kw={'class': 'form-control', 'placeholder': '请输入正文'},
                            validators=[DataRequired('回答不能为空'),
                                        Length(min=5, message='回答至少五个字')])

    def save(self, question):
        """将表单（模态框数据保存）"""
        content = self.content.data
        user = current_user
        answer_obj = Answer(content=content, user=user, question=question)
        db.session.add(answer_obj)
        db.session.commit()
        return answer_obj
