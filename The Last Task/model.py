import datetime
import os
from builtins import ord

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import      \
    Column,                 \
    Integer, String, Date, DateTime,  \
    ForeignKey,             \
    create_engine

from sqlalchemy.orm import          \
    relationship, column_property,  \
    declarative_base


# declarative base class
Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    games = relationship('Game', back_populates="publisher")

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Publisher \"{self.name!r}\">'

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def get_or_create(cls, name, session):
        """Если существует, возвращает существующий экземпляр, иначе создаёт новый"""
        exists = session.query(Publisher.id).filter_by(name=name).scalar()
        if exists:
            return session.query(Publisher).filter_by(name=name).first()

        return cls(name=name)


class Developer(Base):
    __tablename__ = 'developer'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    games = relationship('Game', back_populates="developer")
    # num_games = column_property(select(func.count(games)))

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Developer \"{self.name!r}\">'

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def get_or_create(cls, name, session):
        """Если существует, возвращает существующий экземпляр, иначе создаёт новый"""
        exists = session.query(Developer.id).filter_by(name=name).scalar()
        if exists:
            return session.query(Developer).filter_by(name=name).first()

        return cls(name=name)


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    release_date = Column(Date)
    # etc...

    developer_id = Column("Developer", ForeignKey("developer.id"))
    developer = relationship("Developer", uselist=False, back_populates="games")

    publisher_id = Column("Publisher", ForeignKey("publisher.id"))
    publisher = relationship("Publisher", uselist=False, back_populates="games")

    reviews = relationship('Review', back_populates="game")

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.release_date = kwargs.get('release_date')
        self.developer = kwargs.get('developer')
        self.publisher = kwargs.get('publisher')

    def __repr__(self):
        return f'<Game {self.title!r}, developed by {self.developer!r} in {self.release_date!r}>'

    def __str__(self):
        return f'{self.title}'


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String, unique=True)
    password = Column(String)

    reviews = relationship('Review', back_populates="user")

    def __init__(self, nickname: str, password: str):
        self.nickname = nickname
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.nickname}>"

    def __str__(self):
        return f"{self.nickname}"


class Review(Base):
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    review_text = Column(String)
    rating = Column(Integer)

    date_of_review = Column(DateTime)

    game_id = Column("Game", ForeignKey("game.id"))
    game = relationship('Game', back_populates="reviews")

    user_id = Column("User", ForeignKey("user.id"))
    user = relationship('User', back_populates="reviews")

    def __init__(self, rating: int, review_text: str = None, date_of_review: datetime.datetime = None):
        """
        :param rating: рейтинг игры по 5-тибальной шкале
        :param review_text: по умолчанию пуст
        :param date_of_review: по умолчанию - now()
        """

        self.review_text = review_text
        self.date_of_review = date_of_review or datetime.datetime.now()

        if not 0 <= rating <= 5:
            raise ValueError('Рейтинг должен быть в пределах [0, 5]')
        self.rating = rating

    def __repr__(self):
        return f"<Review from {self.user} to the \"{self.game}\" ({self.rating})>"
