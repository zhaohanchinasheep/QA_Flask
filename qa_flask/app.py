from flask import Flask, render_template

app = Flask(__name__,static_folder="assets")


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
