import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Таблица для связи many-to-many между пользователями и игровыми сессиями
session_participants = sqlalchemy.Table(
    'session_participants',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('session_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('game_sessions.id'))
)

class GameSession(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'game_sessions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('games.id'), nullable=False)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    max_players = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    current_players = sqlalchemy.Column(sqlalchemy.Integer, default=1)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
    status = sqlalchemy.Column(sqlalchemy.String, default="Запланировано")

    game = orm.relationship("Game", back_populates="sessions")
    creator = orm.relationship("User", back_populates="created_sessions")
    participants = orm.relationship('User', 
                                 secondary=session_participants,
                                 backref='participated_sessions')
