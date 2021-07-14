import os

from sqlalchemy import      \
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

    @classmethod
    def get_or_create(cls, name, session):
        """Если существует, возвращает существующий экземпляр, иначе создаёт новый"""
        exists = session.query(Publisher.id).filter_by(name=name).scalar() is not None
        if exists:
            return session.query(Publisher).filter_by(name=name).first()

        return cls(name=name)


class Developer(Base):
    __tablename__ = 'developer'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    games = relationship('Game', back_populates="developer")
    # num_games = column_property(select(func.count(games)))

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def get_or_create(cls, name, session):
        """Если существует, возвращает существующий экземпляр, иначе создаёт новый"""
        exists = session.query(Developer.id).filter_by(name=name).scalar() is not None
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

    def __init__(self, **kwargs):
        self.title = kwargs['title']
        self.release_date = kwargs['release_date']
        self.developer = kwargs['developer']
        self.publisher = kwargs['publisher']


def init_db(path: str, recreate=False):
    """Инициализация ДБ и создание файла-db, если он не существует"""
    if recreate and os.path.exists(path):
        os.remove(path)

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
