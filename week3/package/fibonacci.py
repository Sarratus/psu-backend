from functools import wraps
from time import time
from collections import deque


def fibonacci_generator(limit: int = 10):
    sequence = deque()

    for number_of_element in range(limit):
        if number_of_element == 0:
            element = 0
        if number_of_element == 1:
            element = 1
        if number_of_element >= 2:
            current = number_of_element
            element = sequence[0] + sequence[1]

        sequence.append(element)
        if len(sequence) == 3:
            sequence.popleft()

        yield element


class fibonacciSequence():

    def __init__(self, limit: int = 10):
        self.number_of_element = 0
        self._sequence = deque()

    def __iter__(self):
        return self

    def __next__(self):
        if self.number_of_element == 0:
            element = 0
        if self.number_of_element == 1:
            element = 1
        if self.number_of_element >  1:
            current = self.number_of_element
            element = self._sequence[0] + self._sequence[1]
        if self.number_of_element == 10:
            raise StopIteration

        self.number_of_element += 1

        self._sequence.append(element)
        if len(self._sequence) == 3:
            self._sequence.popleft()

        return element


if __name__ == '__main__':
    fib = fibonacciSequence()
    for elem in fib:
        print(f'№{fib.number_of_element}: \t{elem}')

    gen = fibonacci_generator(limit = 10)
    for _ in range(10):
        print(next(gen))
