from typing import List
from functools import reduce
from random import randint


def str_merge(_list: List[str]) -> str:
    """Соединяет через пробел список строк в одну, приводя к нижнему регистру"""

    func = lambda prev, curr: (prev + ' ' + curr).lower()
    return reduce(func, _list)


def list_filter(_list: List[int]) -> list:
    """Возвращает список чётных элементов из исходного списка"""

    func = lambda item: item % 2 == 0
    return list(filter(func, _list))


def mapping(list1: list) -> list:
    """Преобразует список разных типов в список строк по правилам из encode()"""

    def encode(item) -> str:
        """Пытается преобразовать элемент в строку"""

        item_type = type(item)

        if item_type == str:
            return item
        if item_type == int:
            return chr(item % 1114111)  # 1114111 - максимальный возможный аргумент для chr()
        if item_type == float:
            return str(item)
        if item_type == bool:
            return str(int(item))

        try:
            _ = iter(item)          # Проверка, является ли объект итерируемым

            answer = [encode(i) for i in item]
            return ' '.join(answer)
        except TypeError:
            return 'UNKNOWN TYPE'

    return list(map(encode, list1))


if __name__ == '__main__':
    test_list = ['Hello,', 'WONDERFUL', 'world!']
    print('reduce:\t',  str_merge(test_list))

    test_list = [randint(1, 100) for _ in range(10)]
    print('filter:\t',  list_filter(test_list))

    test_list = [
        21131, 3.14, 'lemon', [1415, [1252, 2.3], 'tomato'], 'lime', (200, 'watermelon'),
        {'peach': True, 'blueberry': 'apple'}, True, {"apple", "banana", "cherry"}, b"Hello"
    ]
    print('map:\t',     mapping(test_list))
