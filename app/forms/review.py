from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from ..data.games import Game


class ReviewForm(FlaskForm):
    game_id = SelectField("Игра",validators=[DataRequired()])
    rating = IntegerField("Оценка (1-5)",validators=[DataRequired(),NumberRange(min=1, max=5)])
    text = TextAreaField("Текст отзыва",validators=[DataRequired()])
    submit = SubmitField("Опубликовать")

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.game_id.choices = [
            (game.id, game.title) for game in Game.query.order_by(Game.title).all()
        ]