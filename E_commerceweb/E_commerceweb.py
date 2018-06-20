# encoding: utf-8
from flask import Flask, render_template, request, redirect, url_for, session, g
import config
from models import User, Question,Answer,Close,close_Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/communication/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/new_close/')
def new_close():
    context1 = {
        'closes': Close.query.order_by('-id').all()
    }
    return render_template('new_close.html', **context1)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # 如果想在31天内都不需要登录
            session.permanent = True
            return redirect(url_for('main'))
        else:
            return u'手机号码或者密码错误，请确认后再登录！'

@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 手机号码验证，如果被注册了，就不能再注册了
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码！'
        else:
            # password1 要和password2相等才可以
            if password1 !=password2:
                return u'两次密码不相等，请核对后再填写！'
            else:
                user = User(telephone=telephone, username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就让页面跳转到登录的页面
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    #session.pop('user_id')
    #del session['user_id']
    session.clear()
    return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        # 如果发布成功，就让页面跳转到问答交流页面
        return redirect(url_for('index'))

@app.route('/close/',methods=['GET','POST'])
@login_required
def close():
    if request.method == 'GET':
        return render_template('close.html')
    else:
        close_name = request.form.get('close_name')
        img = request.form.get('img')
        content = request.form.get('content')
        close_price = request.form.get('close_price')
        num = request.form.get('num')
        close = Close(close_name=close_name, img=img, content=content, close_price=close_price, num=num)
        close.author = g.user
        db.session.add(close)
        db.session.commit()
        # 如果发布成功，就让页面跳转到潮流新品页面
        return redirect(url_for('new_close'))

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)

@app.route('/detail_close/<close_id>')
def detail_close(close_id):
    close_model = Close.query.filter(Close.id == close_id).first()
    return render_template('detail_close.html', close=close_model)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))

@app.route('/close_answer/',methods=['POST'])
@login_required
def close_answer():
    content = request.form.get('close_content')
    close_id = request.form.get('close_id')
    close_answer = close_Answer(content=content)
    close_answer.author = g.user
    close = Close.query.filter(Close.id == close_id).first()
    close_answer.close = close
    db.session.add(close_answer)
    db.session.commit()
    return redirect(url_for('detail_close', close_id=close_id))


@app.route('/communication/search/')
def search():
    q = request.args.get('q')
    # title,content
    # 或
    condition = or_(or_(Question.title.contains(q), Question.content.contains(q)))
    questions = Question.query.filter(condition).order_by('-create_time')
    # 与
    # questions = Question.query.filter(Question.title.contains(q), Question.content.contains(q))
    return render_template('index.html', questions=questions)

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}

# before_request -> 视图函数 -> context_processor
if __name__ == '__main__':
    app.run(host='0.0.0.0')
