import os

from sqlalchemy import  \
    Column,             \
    Integer, String,    \
    ForeignKey,         \
    create_engine

from sqlalchemy.orm import  \
    relationship,           \
    declarative_base


# declarative base class
Base = declarative_base()


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    developer_id = relationship("Developer", ForeignKey("developer.id"))
    developer = relationship("Developer", back_populates="games")

    publisher_id = relationship("Publisher", ForeignKey("publisher.id"))
    publisher = relationship("Publisher", back_populates="games")

    genre = Column(String)


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    games = relationship('Game', back_populates="publisher")


class Developer(Base):
    __tablename__ = 'developer'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    games = relationship('Game', back_populates="developer")


if __name__ == '__main__':
    path_to_db = 'test.db'

    engine = create_engine(f'sqlite:///{path_to_db}')

    if os.path.exists(path_to_db):
        os.remove(path_to_db)
        print('DB has been recreated.')

    Base.metadata.create_all(engine)
