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


if __name__ == '__main__':
    test_list = ['Hello,', 'WONDERFUL', 'world!']
    print('reduce:\t', str_merge(test_list))

    test_list = [randint(1, 100) for _ in range(10)]
    print('filter:\t', list_filter(test_list))
