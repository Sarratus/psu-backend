from dbSetup import init_db, Game, Publisher, Developer
from sqlalchemy import select
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


def fill_db(games: list, session: Session) -> None:
    """Заполняет DB данными из словаря подобного таблице <game>"""
    for game in games:
        title = game['title']
        date = game['release_date']
        developer = Developer(game['developer'])
        publisher = Publisher(game['publisher'])

        _game = Game(title=title, release_date=date, publisher=publisher, developer=developer)
        session.add(_game)

    session.commit()


if __name__ == '__main__':
    games = parse_txt('data.txt')

    engine = init_db('test.db')
