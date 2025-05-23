from flask import Flask, request, session, send_file, flash, redirect, url_for, jsonify, abort, render_template
from data import db_session
from data.users import User
from data.games import Game
from forms.user import RegisterForm, LoginForm
from forms.game import GameForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.game_session import GameSessionForm
from data.game_sessions import GameSession
from data.reviews import Review
import datetime
import os
from io import BytesIO
from urllib.parse import quote
import requests
from sqlalchemy.orm import joinedload

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
    user = db_sess.get(User, user_id)
    db_sess.close()
    return user

YANDEX_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"


def geocode_address(address):
    """Функция для геокодирования адреса через Яндекс.API"""
    try:
        encoded_address = quote(address)
        geocode_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_API_KEY}&geocode={encoded_address}&format=json"
        response = requests.get(geocode_url, timeout=5)
        response.raise_for_status()
        data = response.json()
        features = data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', [])
        if not features:
            return None

        pos = features[0]['GeoObject']['Point']['pos']
        longitude, latitude = map(float, pos.split())

        precision = features[0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['precision']
        is_exact = precision in ['exact', 'number', 'near', 'range']

        return {
            'latitude': latitude,
            'longitude': longitude,
            'zoom': 15 if is_exact else 12,
            'is_exact': is_exact,
            'location_query': address
        }

    except Exception as e:
        print(f"Ошибка геокодирования: {str(e)}")
        return None

@app.route("/")
def index():
    db_sess = db_session.create_session()
    query = db_sess.query(Game).options(joinedload(Game.user), joinedload(Game.reviews))

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

    # Вычисляем средний рейтинг для каждой игры
    for game in games:
        if game.reviews:
            game.rating = round(sum(review.rating for review in game.reviews) / len(game.reviews), 1)
        else:
            game.rating = 0

    db_sess.close()
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


@app.route('/game_image/<int:game_id>')
def game_image(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).get(game_id)
    if game and game.image:
        return send_file(
            BytesIO(game.image),
            mimetype='image/jpeg'
        )
    return abort(404)


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

        if form.image.data:
            image_data = form.image.data.read()
            game.image = image_data

        db_sess.add(game)
        db_sess.commit()
        return redirect('/')
    return render_template('games.html', title='Добавление игры', form=form)


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

            if form.image.data:
                image_data = form.image.data.read()
                game.image = image_data

            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('games.html', title='Редактирование игры', form=form)


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
        try:
            genres = db_sess.query(Game.genre).distinct().all()
            return [genre[0] for genre in genres if genre[0]]
        finally:
            db_sess.close()

    return dict(get_unique_genres=get_unique_genres)


def update_session_statuses(db_sess):
    """Обновляет статусы игровых встреч"""
    current_datetime = datetime.datetime.now()

    sessions = db_sess.query(GameSession).filter(
        GameSession.status == "Запланировано"
    ).all()

    for session in sessions:
        session_datetime = datetime.datetime.combine(session.date, session.time)

        if current_datetime > session_datetime:
            session.status = "Завершено"

    db_sess.commit()


@app.route('/game_sessions')
def game_sessions():
    db_sess = db_session.create_session()
    try:
        update_session_statuses(db_sess)

        if current_user.is_authenticated:
            query = db_sess.query(GameSession).options(
                joinedload(GameSession.game),
                joinedload(GameSession.creator)
            ).filter(
                GameSession.location.like(f"%{current_user.location}%")
            )
            query = query.filter(
                (GameSession.status != "Завершено") | 
                (GameSession.creator_id == current_user.id)
            )
            
            sessions = query.order_by(GameSession.date).all()
        else:
            sessions = []
        return render_template('game_sessions.html', sessions=sessions)
    finally:
        db_sess.close()


@app.route('/game_sessions/new', methods=['GET', 'POST'])
@login_required
def game_session_new():
    form = GameSessionForm()
    db_sess = db_session.create_session()
    try:
        games = db_sess.query(Game).all()
        form.game.choices = [(g.id, g.title) for g in games]

        # Устанавливаем город пользователя как значение по умолчанию
        if request.method == "GET":
            form.location.data = current_user.location or ""

        if form.validate_on_submit():
            session = GameSession(
                game_id=form.game.data,
                date=form.date.data,
                time=form.time.data,
                location=form.location.data,
                description=form.description.data,
                max_players=form.max_players.data,
                creator_id=current_user.id,
                current_players=1,
                status="Запланировано"
            )
            session.participants.append(current_user)
            db_sess.add(session)
            db_sess.commit()
            flash('Игровая встреча успешно создана!', 'success')
            return redirect('/game_sessions')
    except Exception as e:
        db_sess.rollback()
        flash(f'Ошибка при создании встречи: {str(e)}', 'danger')
    finally:
        db_sess.close()

    return render_template('game_session_form.html',
                           title='Новая встреча',
                           form=form)


@app.route('/game_sessions/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def game_sessions_edit(id):
    form = GameSessionForm()
    db_sess = db_session.create_session()
    try:
        games = db_sess.query(Game).all()
        form.game.choices = [(g.id, g.title) for g in games]

        session = db_sess.query(GameSession).filter(
            GameSession.id == id,
            GameSession.creator_id == current_user.id
        ).first()

        if not session:
            abort(404)

        if request.method == "GET":
            form.game.data = session.game_id
            form.date.data = session.date
            form.time.data = session.time
            form.description.data = session.description
            form.max_players.data = session.max_players

        if form.validate_on_submit():
            session.game_id = form.game.data
            session.date = form.date.data
            session.time = form.time.data
            session.description = form.description.data
            session.max_players = form.max_players.data

            db_sess.commit()
            flash('Встреча успешно обновлена!', 'success')
            return redirect('/game_sessions')

        return render_template('game_session_form.html',
                               title='Редактирование встречи',
                               form=form)
    finally:
        db_sess.close()

    return redirect('/game_sessions')


@app.route('/game_sessions/<int:id>/delete', methods=['POST'])
@login_required
def game_sessions_delete(id):
    db_sess = db_session.create_session()
    try:
        session = db_sess.query(GameSession).filter(
            GameSession.id == id,
            GameSession.creator_id == current_user.id
        ).first()

        if session:
            db_sess.delete(session)
            db_sess.commit()
            flash('Встреча успешно удалена!', 'success')
        else:
            abort(404)
    finally:
        db_sess.close()
    return redirect('/game_sessions')


@app.route('/game_sessions/<int:id>/join', methods=['POST'])
@login_required
def game_sessions_join(id):
    db_sess = db_session.create_session()
    try:
        session = db_sess.get(GameSession, id)

        if not session:
            abort(404)

        # Проверяем, не является ли пользователь уже участником
        if current_user in session.participants:
            flash('Вы уже участвуете в этой встрече!', 'warning')
            return redirect('/game_sessions')

        if session.current_players >= session.max_players:
            flash('К сожалению, все места уже заняты.', 'warning')
        else:
            session.participants.append(current_user)
            session.current_players += 1
            db_sess.commit()
            flash('Вы успешно присоединились к встрече!', 'success')
    finally:
        db_sess.close()
    return redirect('/game_sessions')


@app.route('/game_sessions/<int:id>/leave', methods=['POST'])
@login_required
def game_sessions_leave(id):
    db_sess = db_session.create_session()
    try:
        session = db_sess.get(GameSession, id)

        if not session:
            abort(404)

        if current_user in session.participants:
            session.participants.remove(current_user)
            session.current_players -= 1
            db_sess.commit()
            flash('Вы успешно покинули встречу!', 'success')
        else:
            flash('Вы не являетесь участником этой встречи!', 'warning')
    finally:
        db_sess.close()
    return redirect('/game_sessions')


@app.route('/game/<int:id>')
def game_page(id):
    db_sess = db_session.create_session()
    game = db_sess.get(Game, id, options=[joinedload(Game.reviews)])
    if not game:
        abort(404)

    # Вычисляем средний рейтинг
    if game.reviews:
        game.rating = round(sum(review.rating for review in game.reviews) / len(game.reviews), 1)
    else:
        game.rating = 0

    return render_template('game_page.html', game=game, reviews=game.reviews)


@app.route('/game/<int:game_id>/review', methods=['POST'])
@login_required
def add_review(game_id):
    db_sess = db_session.create_session()
    try:
        game = db_sess.get(Game, game_id)
        if not game:
            abort(404)

        # Проверяем, не оставлял ли пользователь уже отзыв
        existing_review = db_sess.query(Review).filter(
            Review.game_id == game_id,
            Review.user_id == current_user.id
        ).first()

        if existing_review:
            flash('Вы уже оставляли отзыв к этой игре', 'warning')
            return redirect(url_for('game_page', id=game_id))

        review = Review(
            text=request.form['text'],
            rating=int(request.form['rating']),
            game_id=game_id,
            user_id=current_user.id
        )

        db_sess.add(review)
        db_sess.commit()
        flash('Ваш отзыв успешно добавлен!', 'success')

    finally:
        db_sess.close()
    return redirect(url_for('game_page', id=game_id))


@app.route('/game_sessions/<int:id>')
def game_session_detail(id):
    db_sess = db_session.create_session()
    try:
        session = db_sess.get(GameSession, id)
        if not session:
            abort(404)
        coordinates = geocode_address(session.location)

        # Если геокодирование не удалось, используем центр Кургана
        if not coordinates:
            coordinates = {
                'latitude': 55.441004,
                'longitude': 65.341118,
                'zoom': 12,
                'is_exact': False,
                'location_query': session.location
            }

        return render_template(
            'game_session_detail.html',
            title='Детали встречи',
            session=session,
            map_coordinates=coordinates
        )
    finally:
        db_sess.close()

@app.route('/check_upcoming_games')
@login_required
def check_upcoming_games():
    # Проверяем, когда было последнее уведомление
    last_notification = session.get('last_notification_time')
    current_time = datetime.datetime.now()

    if last_notification:
        last_notification = datetime.datetime.fromisoformat(last_notification)
        # Если прошло меньше часа, не показываем уведомление
        if (current_time - last_notification).total_seconds() < 20:
            return jsonify({'upcoming_games': []})

    db_sess = db_session.create_session()
    try:
        # Получаем встречи на завтра для текущего пользователя
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        upcoming_games = db_sess.query(GameSession).join(
            GameSession.participants
        ).options(
            joinedload(GameSession.game)
        ).filter(
            GameSession.date == tomorrow,
            GameSession.participants.any(id=current_user.id)
        ).all()

        # Если есть предстоящие игры, обновляем время последнего уведомления
        if upcoming_games:
            session['last_notification_time'] = current_time.isoformat()

        # Формируем список встреч для отправки
        games_data = [{
            'game_title': session.game.title,
            'time': session.time.strftime('%H:%M'),
            'location': session.location
        } for session in upcoming_games]

        return jsonify({'upcoming_games': games_data})
    finally:
        db_sess.close()


@app.route('/test_notification')
@login_required
def test_notification():
    """Тестовый маршрут для проверки уведомлений"""
    return render_template('test_notification.html')


def main():
    db_session.global_init("db/boardgames.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
