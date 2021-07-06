from dbSetup import init_db, Game, Publisher, Developer
from sqlalchemy import select, func, update
from sqlalchemy.orm import Session
from datetime import datetime


def parse_txt(path: str) -> list:
    """
    Парсит .txt (сохраняю в нём данные о играх) файл в словарь

    :param path: путь к файлу с данными
    :return: массив словарей (каждый - одна игра) подобный строке таблицы game
    """

    with open(path) as file:
        games = []
        i, j = -1, 0
        for line in file:
            line = line[:-1]  # обрезаем '\n'

            if line[0] != ' ':
                # Если нет отступа - название новой (следующей) игры
                i += 1
                games.append({'title': line})
                continue

            # Иначе - данные о ней
            line = line[3:]  # обрезаем табуляцию

            if j == 0:
                date = datetime.strptime(line[1:], '%d.%m.%Y').date()
                games[i]['release_date'] = date

            if j == 1:
                games[i]['developer'] = line[1:]

            if j == 2:
                games[i]['publisher'] = line[1:]
                j = -1

            j += 1

    return games


def add_entry(session: Session, **entry) -> None:
    if not isinstance(entry['developer'], Developer):
        entry['developer'] = Developer.get_or_create(entry['developer'], session)
    if not isinstance(entry['publisher'], Publisher):
        entry['publisher'] = Publisher.get_or_create(entry['publisher'], session)

    game = Game(**entry)

    session.add(game)
    session.commit()


if __name__ == '__main__':
    games = parse_txt('data.txt')
    engine = init_db('test.db', recreate=True)

    with Session(engine) as session:
        # Запонение базы данными из файла
        if not session.query(Game).all():
            [add_entry(session, **game) for game in games]
            session.commit()

        # Обновление одной из записей (замена имени разработчика)
        session.query(Developer) \
            .filter(Developer.name == 'Silicon & Synapse') \
            .update({Developer.name: 'Blizzard Entertainment'})
        session.commit()

        # Удаление одной из записей
        i = session.query(Developer).filter_by(name='Interplay Productions').one()
        session.delete(i)
        session.commit()

        # Количество разработчиков
        session.query(func.count(Developer.id)).all()

        # Издатели с выпущенными играми
        session.query(Publisher).join(Publisher.games).all()

        # Названия разработчиков с более чем одной выпущенной игрой
        i = session.query(Developer.name)\
            .join(Developer.games)\
            .group_by(Developer.id)\
            .having(func.count(Game.id) > 1)\
            .all()
        print(*[it[0] for it in i], sep=', ')

        # Получение списка всех разработчиков
        stmt = select('*').select_from(Developer)
        print(*[i[1] for i in engine.execute(stmt).all()], sep=', ')



    # with Session(engine) as session:
    #     fill_db(games, session)
    #
    #     stmt = select(func.count(Publisher.id)).select_from(Publisher)
    #     print(engine.execute(stmt).all())
    #
    #     stmt = select('*').select_from(Publisher)
    #     print(engine.execute(stmt).all())
