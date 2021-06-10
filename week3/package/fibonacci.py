from functools import wraps
from time import time, sleep
from collections import deque
from inspect import signature


def types_checker(*types):
    """
    Декоратор, предопределяющий типы аргументов функции.
    Выводит краткую информацию о функции: название, кол-во аргументов, время исполнения.
    """

    def stats(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # from python.org/dev/peps/pep-0318/#examples
            assert len(types) == func.__code__.co_argcount
            for passed, intended in zip(args, types):
                assert isinstance(passed, intended), f"argument {passed} doesn't match {intended}"

            func_name = func.__name__
            func_num_of_args = func.__code__.co_argcount
            func_signature = signature(func)

            print(f'Function \'{func_name}\' is executed...\n'
                  f'Its signature is {func_signature}, {func_num_of_args} arg(s)')

            start = time()
            result = func(*args, **kwargs)
            exec_time = time() - start

            print(f'Time of execution: {exec_time} s.')

            return result
        return wrapper
    return stats


@types_checker(int, (str, list))
def foo(x: int, y: str = 'bar'):
    """Важная и сложная функция."""
    sleep(1.173)
    return None


def fibonacci_generator(limit: int = 10):
    """Генератор чисел Фибоначчи."""
    sequence = deque()

    for number_of_element in range(limit):
        if number_of_element == 0:
            element = 0
        if number_of_element == 1:
            element = 1
        if number_of_element >= 2:
            element = sequence[0] + sequence[1]

        sequence.append(element)
        if len(sequence) == 3:
            sequence.popleft()

        yield element


class FibonacciSequence:
    def __init__(self, limit: int = 10):
        self.number_of_element = 0
        self.limit = limit
        # Используется двунаправленная очередь для хранения 2ух последних чисел Фибоначчи
        self._sequence = deque(maxlen=3)

    def __iter__(self):
        return self

    def __next__(self):
        if self.number_of_element == 0:
            element = 0
        if self.number_of_element == 1:
            element = 1
        if self.number_of_element >= 2:
            element = self._sequence[0] + self._sequence[1]
        if self.number_of_element == self.limit:
            raise StopIteration

        self._sequence.append(element)
        if len(self._sequence) == 3:    # Для экономии памяти числа старше 2ого поколения удаляются
            self._sequence.popleft()

        self.number_of_element += 1
        return element


if __name__ == '__main__':
    fib = FibonacciSequence(10)
    for elem in fib:
        print(f'№{fib.number_of_element - 1}: \t{elem}')

    print()

    gen = fibonacci_generator(limit=10)
    for i in range(10):
        print(f'№{i}: \t{next(gen)}')

    print()

    foo(1, 'foo')
