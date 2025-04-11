from data import db_session
from data.users import User
from data.games import Game
import random

def add_test_data():
    db_sess = db_session.create_session()

    # Создаем 6 пользователей
    users = [
        {
            "name": "Иван",
            "surname": "Иванов",
            "age": 25,
            "email": "ivan@example.com",
            "favorite_genres": "Стратегия, Экономика",
            "location": "Москва",
            "password": "ivan123"
        },
        {
            "name": "Петр",
            "surname": "Петров",
            "age": 30,
            "email": "petr@example.com",
            "favorite_genres": "Приключения, Фэнтези",
            "location": "Санкт-Петербург",
            "password": "petr123"
        },
        {
            "name": "Анна",
            "surname": "Сидорова",
            "age": 28,
            "email": "anna@example.com",
            "favorite_genres": "Кооператив, Детектив",
            "location": "Екатеринбург",
            "password": "anna123"
        },
        {
            "name": "Мария",
            "surname": "Козлова",
            "age": 22,
            "email": "maria@example.com",
            "favorite_genres": "Карточные, Семейные",
            "location": "Новосибирск",
            "password": "maria123"
        },
        {
            "name": "Алексей",
            "surname": "Смирнов",
            "age": 35,
            "email": "alex@example.com",
            "favorite_genres": "Военные, Исторические",
            "location": "Казань",
            "password": "alex123"
        },
        {
            "name": "Елена",
            "surname": "Волкова",
            "age": 27,
            "email": "elena@example.com",
            "favorite_genres": "Партийные, Логические",
            "location": "Ростов-на-Дону",
            "password": "elena123"
        }
    ]

    # Добавляем пользователей в базу данных
    for user_data in users:
        user = User(
            name=user_data["name"],
            surname=user_data["surname"],
            age=user_data["age"],
            email=user_data["email"],
            favorite_genres=user_data["favorite_genres"],
            location=user_data["location"]
        )
        user.set_password(user_data["password"])
        db_sess.add(user)
    
    db_sess.commit()

    # Получаем ID всех пользователей
    user_ids = [user.id for user in db_sess.query(User).all()]

    # Создаем 20 игр
    games = [
        {
            "title": "Монополия",
            "duration": "2-3 часа",
            "count_of_players": "2-6",
            "genre": "Экономика",
            "complexity": "Средняя",
            "description": "Классическая экономическая игра"
        },
        {
            "title": "Каркассон",
            "duration": "30-45 минут",
            "count_of_players": "2-5",
            "genre": "Стратегия",
            "complexity": "Легкая",
            "description": "Стратегическая игра с плитками"
        },
        {
            "title": "Манчкин",
            "duration": "1-2 часа",
            "count_of_players": "3-6",
            "genre": "Карточные",
            "complexity": "Легкая",
            "description": "Юмористическая карточная игра"
        },
        {
            "title": "Колонизаторы",
            "duration": "1-2 часа",
            "count_of_players": "3-4",
            "genre": "Стратегия",
            "complexity": "Средняя",
            "description": "Стратегическая игра с ресурсами"
        },
        {
            "title": "Эволюция",
            "duration": "1 час",
            "count_of_players": "2-4",
            "genre": "Стратегия",
            "complexity": "Средняя",
            "description": "Игра о развитии видов"
        },
        {
            "title": "Алиас",
            "duration": "30-60 минут",
            "count_of_players": "4-12",
            "genre": "Партийные",
            "complexity": "Легкая",
            "description": "Игра на объяснение слов"
        },
        {
            "title": "Доминион",
            "duration": "30 минут",
            "count_of_players": "2-4",
            "genre": "Карточные",
            "complexity": "Средняя",
            "description": "Коллекционная карточная игра"
        },
        {
            "title": "7 чудес",
            "duration": "30 минут",
            "count_of_players": "2-7",
            "genre": "Стратегия",
            "complexity": "Средняя",
            "description": "Стратегическая игра о строительстве чудес"
        },
        {
            "title": "Кодовые имена",
            "duration": "15 минут",
            "count_of_players": "4-8",
            "genre": "Партийные",
            "complexity": "Легкая",
            "description": "Командная игра на ассоциации"
        },
        {
            "title": "Терра Мистика",
            "duration": "2-3 часа",
            "count_of_players": "2-5",
            "genre": "Стратегия",
            "complexity": "Высокая",
            "description": "Сложная стратегическая игра"
        },
        {
            "title": "Пандемия",
            "duration": "45 минут",
            "count_of_players": "2-4",
            "genre": "Кооператив",
            "complexity": "Средняя",
            "description": "Кооперативная игра о спасении мира"
        },
        {
            "title": "Шакал",
            "duration": "1-2 часа",
            "count_of_players": "2-4",
            "genre": "Приключения",
            "complexity": "Легкая",
            "description": "Игра о поиске сокровищ"
        },
        {
            "title": "Мемо",
            "duration": "15 минут",
            "count_of_players": "2-6",
            "genre": "Семейные",
            "complexity": "Легкая",
            "description": "Игра на память"
        },
        {
            "title": "Скрэббл",
            "duration": "1 час",
            "count_of_players": "2-4",
            "genre": "Логические",
            "complexity": "Средняя",
            "description": "Игра в слова"
        },
        {
            "title": "Уно",
            "duration": "15-30 минут",
            "count_of_players": "2-10",
            "genre": "Карточные",
            "complexity": "Легкая",
            "description": "Популярная карточная игра"
        },
        {
            "title": "Цитадели",
            "duration": "30-60 минут",
            "count_of_players": "2-8",
            "genre": "Стратегия",
            "complexity": "Средняя",
            "description": "Стратегическая игра о строительстве города"
        },
        {
            "title": "Экивоки",
            "duration": "1 час",
            "count_of_players": "4-16",
            "genre": "Партийные",
            "complexity": "Легкая",
            "description": "Игра на объяснение слов разными способами"
        },
        {
            "title": "Манчкин Квест",
            "duration": "1-2 часа",
            "count_of_players": "2-4",
            "genre": "Приключения",
            "complexity": "Средняя",
            "description": "Приключенческая версия Манчкина"
        },
        {
            "title": "Свинтус",
            "duration": "15-30 минут",
            "count_of_players": "2-10",
            "genre": "Карточные",
            "complexity": "Легкая",
            "description": "Веселая карточная игра"
        },
        {
            "title": "Колонизаторы: Города и Рыцари",
            "duration": "2-3 часа",
            "count_of_players": "3-4",
            "genre": "Стратегия",
            "complexity": "Высокая",
            "description": "Расширение для Колонизаторов"
        }
    ]

    # Добавляем игры в базу данных со случайным распределением по пользователям
    for game_data in games:
        game = Game(
            title=game_data["title"],
            duration=game_data["duration"],
            count_of_players=game_data["count_of_players"],
            genre=game_data["genre"],
            complexity=game_data["complexity"],
            description=game_data["description"],
            added_by=random.choice(user_ids)  # Случайный выбор пользователя
        )
        db_sess.add(game)
    
    db_sess.commit()

if __name__ == '__main__':
    db_session.global_init("db/boardgames.db")
    add_test_data() 