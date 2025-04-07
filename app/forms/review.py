from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class ReviewForm(FlaskForm):
    game_id = SelectField("Игра",validators=[DataRequired()])
    rating = IntegerField("Оценка (1-5)",validators=[DataRequired(),NumberRange(min=1, max=5)])
    text = TextAreaField("Текст отзыва",validators=[DataRequired()])
    submit = SubmitField("Опубликовать")