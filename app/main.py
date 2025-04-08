import datetime

from flask import Flask, request, make_response, session, abort
from data import db_session
from data.users import User
from data.games import Game
from flask import render_template, redirect
from forms.user import RegisterForm, LoginForm
from forms.game import GameForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)



@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        games = db_sess.query(Game).filter(
            (Game.user == current_user) | (Game.is_private != True))
    else:
        games = db_sess.query(Game).filter(Game.is_private != True)
    # news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", games=games)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login_3.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_3.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/games',  methods=['GET', 'POST'])
@login_required
def add_games():
    form = GameForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        games = Game()
        games.title = form.title.data
        games.content = form.content.data
        games.is_private = form.is_private.data
        current_user.news.append(games)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('games.html', title='Добавление новости',
                           form=form)

@app.route('/games/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = GameForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        games = db_sess.query(Game).filter(Game.id == id,
                                          Game.user == current_user
                                          ).first()
        if games:
            form.title.data = games.title
            form.content.data = games.content
            form.is_private.data = games.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        games = db_sess.query(Game).filter(Game.id == id,
                                          Game.user == current_user
                                          ).first()
        if games:
            games.title = form.title.data
            games.content = form.content.data
            games.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('games.html',
                           title='Редактирование новости',
                           form=form
                           )

@app.route('/games_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def games_delete(id):
    db_sess = db_session.create_session()
    games = db_sess.query(Game).filter(Game.id == id,
                                      Game.user == current_user
                                      ).first()
    if games:
        db_sess.delete(games)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

def main():
    db_session.global_init("db/blogs.db")
    # user = User()
    # user.name = "Пользователь 1"
    # user.about = "биография пользователя 1"
    # user.email = "email@email.ru"
    # user2 = User()
    # user2.name = "Пользователь 2"
    # user2.about = "биография пользователя 2"
    # user2.email = "email2@email.ru"
    # user3 = User()
    # user3.name = "Пользователь 3"
    # user3.about = "биография пользователя 3"
    # user3.email = "email3@email.ru"
    # db_sess = db_session.create_session()
    # db_sess.add(user)
    # db_sess.add(user2)
    # db_sess.add(user3)
    # db_sess.commit()
    # news = News(title="Первая новость", content="Привет блог!",
    #             user_id=1, is_private=False)
    # db_sess.add(news)
    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Вторая новость", content="Уже вторая запись!",
    #             user=user, is_private=False)
    # db_sess.add(news)
    # user = db_sess.query(User).filter(User.id == 1).first()
    # news = News(title="Личная запись", content="Эта запись личная",
    #             is_private=True)
    # user.news.append(news)
    # db_sess.commit()
    app.run()


if __name__ == '__main__':
    main()