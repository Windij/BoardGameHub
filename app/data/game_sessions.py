import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class GameSession(SqlAlchemyBase):
    __tablename__ = 'game_sessions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('games.id'), nullable=False)
    organizer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    max_participants = sqlalchemy.Column(sqlalchemy.Integer)
    status = sqlalchemy.Column(sqlalchemy.String, default="Запланировано")  # Запланировано/Завершено

    game = orm.relationship("Game", back_populates="sessions")
    organizer = orm.relationship("User", back_populates="organized_sessions")