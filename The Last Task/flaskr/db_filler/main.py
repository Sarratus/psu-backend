from ..model import Game, Publisher, Developer
from datetime import datetime
from typing import List


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


def add_entry(session, **entry: List[Game]) -> None:
    # создаёт класс Developer/Publisher, если переданы str(названия), а не экземпляры классов
    if not isinstance(entry['developer'], Developer):
        entry['developer'] = Developer.get_or_create(entry['developer'], session)
    if not isinstance(entry['publisher'], Publisher):
        entry['publisher'] = Publisher.get_or_create(entry['publisher'], session)

    game = Game(**entry)

    session.add(game)
    session.commit()


def fill_out_db(session, num_of_entries=None):
    from os import path
    games = parse_txt(
        path.abspath(
            path.join('flaskr', 'db_filler', 'data.txt')
        )
    )

    if num_of_entries:
        num_of_entries = len(games) if num_of_entries > len(games) else num_of_entries
        games = games[:num_of_entries]

    # Запонение базы данными из файла
    if not session.query(Game).all():
        [add_entry(session, **game) for game in games]
        session.commit()
