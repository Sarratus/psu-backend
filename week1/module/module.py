from re import split
from bisect import bisect_right
from math import inf as INF
from string import punctuation


__all__ = ['list_to_dict', 'strings_interspec', 'longest_ascending_seq']


def list_to_dict(_list: list) -> dict:
    """Приводит массив к словарю вида {элемент: кол-во вхождений}"""

    # Счётчик вхождений target_item в _list
    def counter(target_item) -> int:
        number_of_items = sum(
            1 for element in _list if element == target_item
        )
        return number_of_items

    _dict = {element: counter(element) for element in _list}
    return _dict


def strings_interspec(str1: str, str2: str) -> set:
    """Поиск совпадающих слов в двух строках"""

    # Функция создания последовательности всех слов, входящих в _str
    def all_unique_words(_str: str) -> set:
        list_of_words = [
            word.strip(punctuation).lower()
            for word in _str.split()
        ]
        set_of_words = set(list_of_words)

        return set_of_words

    str1_words = all_unique_words(str1)
    str2_words = all_unique_words(str2)

    # Поиск пересечения множеств слов первой и второй строки
    unique_words_intersection = str2_words.intersection(str1_words)

    return unique_words_intersection


def longest_ascending_seq(_list: list) -> list:
    """Поиск наибольшей возрастающей последовательности из массива целых чисел"""

    n = len(_list)

    F = [-INF] + [INF] * (n+1)
    temp = []

    for item in _list:
        # Бинарный поиск индекса первого элемента в массиве F, который больше item
        right = bisect_right(F, item)
        F[right] = item

        temp.append(F[right - 1])

    # Длина наибольшей возрастающей последовательности
    length = F.index(INF) - 1

    sequence = [None] * length
    k = F[length]

    # Восстановление последовательности
    for i in range(length):
        sequence[i] = _list[k]
        k = temp[k]

    return sequence[::-1]
