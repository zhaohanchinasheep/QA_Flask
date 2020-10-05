import os


class Config(object):
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Admin@123456@localhost/qa_flask'
    # flash ,form wtf
    SECRET_KEY = 'wouldyoubemyhoney'
    # 自定义上传图片路径
    MEDIA_ROOT = os.path.join(os.path.dirname(__file__),'medias')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

