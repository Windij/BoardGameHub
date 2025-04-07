from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class GameSessionForm(FlaskForm):
    game_id = IntegerField("Id игры", validators=[DataRequired()])
    location = StringField("Место проведения", validators=[DataRequired()])
    max_participants = IntegerField("Максимум участников", validators=[DataRequired()])
    status = SelectField("Статус",choices=[("Запланировано", "Запланировано"), ("Завершено", "Завершено")])
    submit = SubmitField("Сохранить")
