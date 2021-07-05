import datetime
import os

from sqlalchemy import      \
    select, func,           \
    Column,                 \
    Integer, String, Date,  \
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
    name = Column(String)

    games = relationship('Game', back_populates="publisher")

    def __init__(self, name: str):
        self.name = name


class Developer(Base):
    __tablename__ = 'developer'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    games = relationship('Game', back_populates="developer")
    # num_games = column_property(select(func.count(games)))

    def __init__(self, name: str):
        self.name = name


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    title = Column(String)

    release_date = Column(Date)
    # etc...

    developer_id = Column("Developer", ForeignKey("developer.id"))
    developer = relationship("Developer", back_populates="games")

    publisher_id = Column("Publisher", ForeignKey("publisher.id"))
    publisher = relationship("Publisher", back_populates="games")

    def __init__(self, title: str, release_date: datetime.date, developer: Developer, publisher: Publisher):
        self.title = title
        self.release_date = release_date
        self.developer = developer
        self.publisher = publisher


def init_db(path: str):
    """Инициализация ДБ и создание файла-db, если он не существует"""
    engine = create_engine(f'sqlite:///{path}')

    if not os.path.exists(path):
        Base.metadata.create_all(engine)

    return engine


if __name__ == '__main__':
    """Reinit DB"""
    path_to_db = 'test.db'

    if os.path.exists(path_to_db):
        os.remove(path_to_db)
        print(f'DB has been recreated in \'.\\{path_to_db}\'')

    init_db(path_to_db)
