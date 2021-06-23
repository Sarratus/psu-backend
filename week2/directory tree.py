import os
import argparse
import sys


def convert_bytes(num: float) -> str:
    """Функция переводит байты в большие величины для лучшей читаемости"""

    for x in ['B', 'KB', 'MB']:
        if num < 1024.0:
            return f'{num:.1f} {x}'
        num /= 1024.0

    return f'{num:.1f} GB'


def make_indent(level: int, is_folder: bool = False) -> str:
    """Возвращает правильный отступ в зависимости от уровня каталога относительно корневого"""

    _indent = '    ' * (level - 1)

    if is_folder:
        _indent += '    '
    else:
        _indent += '  - '

    return _indent


def list_files(start_path, print_size: bool = True, print_name: bool = True) -> None:
    """Выводит дерево каталогов, начиная со start_path"""

    def file_description(file: str) -> list:
        """Возвращает массив строк с описанием файла"""

        description = []

        if print_size:
            file_path = root_abs_path + os.sep + file

            file_stats = os.stat(file_path)
            file_size = convert_bytes(file_stats.st_size)

            description.append(file_size)

        if print_name:
            description.append(file)

        return description

    for root, dirs, files in os.walk(start_path):
        dir_level = root.replace(start_path, '').count(os.sep)
        print('{}{}/'.format(make_indent(dir_level, is_folder=True), os.path.basename(root)))

        root_abs_path = os.path.abspath(root)

        if print_name or print_size:
            [
                print(
                    make_indent(dir_level+1) +
                    '\t| '.join(file_description(file))
                )
                for file in files
            ]


def create_parser():
    """Создаёт парсер для удобного вызова программы из командной строки с аргументами"""

    parser = argparse.ArgumentParser(description='Программа выводит дерево каталогов')
    parser.add_argument('-s', '--size', action='store_true', help='выводит размер файлов')
    parser.add_argument('-n', '--name', action='store_true', help='выводит имя файлов')

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])

    list_files(os.pardir, print_size=args.size, print_name=args.name)
