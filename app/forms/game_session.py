from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, TimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class GameSessionForm(FlaskForm):
    game = SelectField('Игра', coerce=int, validators=[DataRequired()])
    date = DateField('Дата', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Время', format='%H:%M', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    max_players = IntegerField('Максимальное количество игроков', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
