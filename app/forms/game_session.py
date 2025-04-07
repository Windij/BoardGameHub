from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from ..data.games import Game


class GameSessionForm(FlaskForm):
    game_id = SelectField("Id игры",coerce=int, validators=[DataRequired()])
    location = StringField("Место проведения", validators=[DataRequired()])
    max_participants = IntegerField("Максимум участников", validators=[DataRequired()])
    status = SelectField("Статус",choices=[("Запланировано", "Запланировано"), ("Завершено", "Завершено")])
    submit = SubmitField("Сохранить")

    def __init__(self, *args, **kwargs):
        super(GameSessionForm, self).__init__(*args, **kwargs)
        self.game_id.choices = [
            (game.id, game.title) for game in Game.query.order_by(Game.title).all()
        ]