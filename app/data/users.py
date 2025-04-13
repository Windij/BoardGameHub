import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    # position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # speciality:
    favorite_genres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # address:
    location = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    added_games = orm.relationship("Game", back_populates="user")
    created_sessions = orm.relationship("GameSession", back_populates="creator")
    reviews = orm.relationship('Review', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> {self.id} {self.surname} {self.name} {self.email}'
