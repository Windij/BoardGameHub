from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

class GameForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    duration = StringField('Длительность', validators=[DataRequired()])
    count_of_players = StringField('Количество игроков', validators=[DataRequired()])
    genre = SelectField('Жанр', choices=[('Стратегия', 'Стратегия'), ('Детектив', 'Детектив')])
    complexity = SelectField('Сложность', choices=[('Низкая', 'Низкая'), ('Средняя', 'Средняя'), ('Сложная', 'Сложная')])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Сохранить')