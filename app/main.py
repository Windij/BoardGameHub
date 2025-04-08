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
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    
    # Базовый запрос
    query = db_sess.query(Game)
    
    # Фильтрация по жанру
    genre = request.args.get('genre')
    if genre:
        query = query.filter(Game.genre == genre)
    
    # Поиск по названию и описанию
    search = request.args.get('search')
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Game.title.ilike(search_term)) |
            (Game.description.ilike(search_term))
        )
    
    games = query.all()
    return render_template("index.html", title="Главная", games=games)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
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
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
            favorite_genres=form.favorite_genres.data,
            location=form.location.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/games', methods=['GET', 'POST'])
@login_required
def add_games():
    form = GameForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game = Game()
        game.title = form.title.data
        game.duration = form.duration.data
        game.count_of_players = form.count_of_players.data
        game.genre = form.genre.data
        game.complexity = form.complexity.data
        game.description = form.description.data
        game.added_by = current_user.id
        db_sess.add(game)
        db_sess.commit()
        return redirect('/')
    return render_template('games.html', title='Добавление игры',
                        form=form)


@app.route('/games/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_game(id):
    form = GameForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == id,
                                        Game.added_by == current_user.id).first()
        if game:
            form.title.data = game.title
            form.duration.data = game.duration
            form.count_of_players.data = game.count_of_players
            form.genre.data = game.genre
            form.complexity.data = game.complexity
            form.description.data = game.description
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        game = db_sess.query(Game).filter(Game.id == id,
                                        Game.added_by == current_user.id).first()
        if game:
            game.title = form.title.data
            game.duration = form.duration.data
            game.count_of_players = form.count_of_players.data
            game.genre = form.genre.data
            game.complexity = form.complexity.data
            game.description = form.description.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('games.html',
                        title='Редактирование игры',
                        form=form)


@app.route('/games_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def games_delete(id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == id,
                                      Game.user == current_user).first()
    if game:
        db_sess.delete(game)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.context_processor
def utility_processor():
    def get_unique_genres():
        db_sess = db_session.create_session()
        genres = db_sess.query(Game.genre).distinct().all()
        return [genre[0] for genre in genres if genre[0]]
    return dict(get_unique_genres=get_unique_genres)


def main():
    db_session.global_init("db/blogs.db")
    app.run()


if __name__ == '__main__':
    main()