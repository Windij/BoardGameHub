import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'games'  # jobs

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    added_by = sqlalchemy.Column(  # team_leader
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.id'),
        nullable=False
    )
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # job
    duration = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # work_size
    count_of_players = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # collaborators
    # start_date = sqlalchemy.Column(
    #     sqlalchemy.DateTime,
    #     default=datetime.datetime.now
    # )
    # end_date = sqlalchemy.Column(sqlalchemy.DateTime)
    # is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    complexity = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.LargeBinary, nullable=True)  # BLOB для хранения изображений

    user = orm.relationship("User", back_populates="added_games")
    sessions = orm.relationship("GameSession", back_populates="game")
    reviews = orm.relationship("Review", back_populates="game")

    def __repr__(self):
        return (
            f"<Game> {self.id} {self.title} {self.genre} {self.complexity}")
