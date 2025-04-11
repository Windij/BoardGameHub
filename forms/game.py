from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class GameForm(FlaskForm):
    title = StringField('Название игры', validators=[DataRequired()])
    duration = StringField('Длительность игры', validators=[DataRequired()])
    count_of_players = StringField('Количество игроков', validators=[DataRequired()])
    genre = SelectField('Жанр', choices=[
        ('Стратегия', 'Стратегия'),
        ('Карточные', 'Карточные'),
        ('Партийные', 'Партийные'),
        ('Приключения', 'Приключения'),
        ('Кооператив', 'Кооператив'),
        ('Экономика', 'Экономика'),
        ('Семейные', 'Семейные'),
        ('Логические', 'Логические')
    ], validators=[DataRequired()])
    complexity = SelectField('Сложность', choices=[
        ('Низкая', 'Низкая'),
        ('Средняя', 'Средняя'),
        ('Высокая', 'Высокая')
    ], validators=[DataRequired()])
    description = TextAreaField('Описание игры', validators=[DataRequired()])
    image = FileField('Изображение игры', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Разрешены только изображения!')
    ])
    submit = SubmitField('Сохранить')
