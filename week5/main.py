from math import sin, radians, pi


class AngleError(Exception):
    def __init__(self, message):
        self.message = message


class Parallelogram:
    """Класс, описывающий параллелограм"""
    def __init__(self, first_side, second_side, angle):
        self.a, self.b = first_side, second_side
        self.angle = angle

        self.__smaller_angle = angle if angle <= 90 else 180-angle
        self.__height_to_first_side = self.area() / first_side

    def area(self):
        angle_in_radians = radians(self.angle)
        return self.a * self.b * sin(angle_in_radians)

    @staticmethod
    def is_parallelogram(first_side, second_side, angle):
        if (not angle < 180) or (not angle > 0):
            raise AngleError("Некорректное значение угла")
        if (not first_side > 0) or (not second_side > 0):
            raise ValueError("Длина стороны не может быть отрицательной или нулевой")
        return True

    # Магические методы сравнения (сравнение по площадям)---------------------------------------------------------------

    def __eq__(self, other):
        return self.area() == other.area()

    def __ne__(self, other):
        return self.area() != other.area()

    def __lt__(self, other):
        return self.area() < other.area()

    def __gt__(self, other):
        return self.area() > other.area()

    def __le__(self, other):
        return self.area() <= other.area()

    def __ge__(self, other):
        return self.area() >= other.area()

    # ------------------------------------------------------------------------------------------------------------------

    def __str__(self):
        return f"{self.__class__.__name__}:\n" \
               f"\tСтороны равны {self.a} и {self.b}\n" \
               f"\tУгол между ними - {self.angle :.2f} градусов\n" \
               f"\tПлощадь - {self.area() :.2f}"


class Square(Parallelogram):
    """Класс, описывающий квадрат"""
    def __init__(self, side_length):
        super().__init__(side_length, side_length, 90.)
        self.a = side_length

    def area(self):
        return self.a ** 2

    @staticmethod
    def is_square(side_length):
        if not side_length > 0:
            raise ValueError("Длина стороны не может быть отрицательной или нулевой")

        return True


class Rectangle(Parallelogram):
    """Класс, описывающий квадрат"""
    def __init__(self, first_side, second_side):
        super().__init__(first_side, second_side, 90.)
        self.a, self.b = first_side, second_side

    def area(self):
        return self.a ** 2

    @staticmethod
    def is_rectangle(first_side, second_side):
        super().is_parallelogram(first_side, second_side, 90.)
        return True
