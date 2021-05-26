import string


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
            word.strip(string.punctuation).lower()
            for word in _str.split()
            if word.strip(string.punctuation)
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

    def binary_search(L: int) -> int:
        lo = 1
        hi = L + 1

        while lo < hi - 1:  # Бинарный поиск
            mid = (lo + hi) // 2
            if _list[M[mid]] < _list[i]:
                lo = mid
            else:
                hi = mid

        return lo

    n = len(_list)

    _list = [None] + _list
    M = [None] * (n + 1)
    P = [None] * (n + 1)
    L = 0

    # Поиск наибольшей возрастающей последовательности
    for i in range(1, n + 1):
        if L == 0 or _list[M[1]] >= _list[i]:
            j = 0
        else:
            j = binary_search(L)

        P[i] = M[j]
        if j == L or _list[i] < _list[M[j+1]]:
            M[j+1] = i
            L = max(L, j + 1)

    output = []
    pos = M[L]

    # Восстановление последовательности
    while L > 0:
        output.append(_list[pos])
        pos = P[pos]
        L -= 1

    return output[::-1]
