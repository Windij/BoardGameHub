from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, TimeField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from data.games import Game
from data import db_session


class GameSessionForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(GameSessionForm, self).__init__(*args, **kwargs)
        db_sess = db_session.create_session()
        games = db_sess.query(Game).all()
        self.game.choices = [(g.id, g.title) for g in games]

    game = SelectField('Игра', coerce=int,
                      validators=[DataRequired(message="Выберите игру")])
    
    date = DateField('Дата', 
                    validators=[DataRequired(message="Укажите дату проведения")])
    
    time = TimeField('Время', 
                    validators=[DataRequired(message="Укажите время проведения")])
    
    location = StringField('Место проведения', 
                         validators=[DataRequired(message="Укажите место проведения"), 
                                   Length(max=200, message="Слишком длинный адрес")])
    
    max_players = IntegerField('Максимальное количество участников', 
                             validators=[DataRequired(message="Укажите максимальное количество участников"),
                                       NumberRange(min=2, message="Минимум 2 участника")])
    
    description = TextAreaField('Описание', 
                              validators=[DataRequired(message="Добавьте описание встречи"),
                                        Length(min=10, max=500, message="Описание должно быть от 10 до 500 символов")])
    
    submit = SubmitField('Сохранить')
