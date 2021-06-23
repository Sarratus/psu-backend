import os
import string
import random


_path = 'file.bin'


def create_and_fill(path_to_file: str, num_of_char: int = 50) -> None:
    """Создание бинарного файла .bin и заполнение его случайными данными"""

    if not os.path.exists(path_to_file):
        with open(path_to_file, 'x'):
            pass    # Создаёт файл, если он не существует

    # Заполнение случайными символами
    with open(path_to_file, 'wb') as file:
        possible_characters = string.printable + ' '
        random_string = ''.join(random.choices(possible_characters, k=num_of_char))

        file.write(random_string.encode())


def stats_collecting(path_to_file: str) -> dict:
    """Сбор краткой статистики по информации, заключенной в бинарном файле"""

    with open(path_to_file, 'rb') as file:
        data = file.read().decode()     # Считывание и декодирование строки

        lines_count = 1 + data.count('\n')

        whitespace = ' \t'
        words_count = lines_count + sum(data.count(char) for char in whitespace)

        characters_count = len(data)

        return {'lines': lines_count, 'words': words_count, 'chars': characters_count}


if __name__ == '__main__':
    create_and_fill(_path)
    print(stats_collecting(_path))
