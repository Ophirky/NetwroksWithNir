"""
    Author: Ophir Nevo Michrowski
    DATE: 07/06/2024
    DESCRIPTION: Holds the Square class
"""
from shapes.rect import Rectangle
from shapes.shape import Shape
import random
import logging


class Square(Rectangle):
    """Square Class"""

    def __init__(self, len_of_sides: float, color: str) -> None:
        """
        Initializer of the Square class
        :param len_of_sides: The length of all the sides of the square.
        :param color: The color of the square.
        """
        super().__init__(len_of_sides, len_of_sides, color)
        self.color = color
        self.sides = len_of_sides

    def __add__(self, other: Shape) -> Shape:
        """
        Function to handle addition of two shapes.
        :param other: shape that is either a Square or Rectangle.
        :return: new Shape that its area and perimeter are equal to the sum of the sum of the area and perimeter
                 of the two shapes added.
        """
        # Inheriting classes will also return True as an instance of Rectangle
        if not isinstance(other, Rectangle):
            raise ValueError("Rectangle can only be asses with other Rectangles!")

        width, length = self._find_rectangle_dimensions(self.get_area() + other.get_area(),
                                                        self.get_perimeter() + other.get_perimeter())

        res: Shape
        if width != length:
            res = Rectangle(width, length, random.choice((self.color, other.color)))
            logging.info(f"Created new rectangle with width: {width}, height: {length}, color: {res.color}")
        else:
            res = Square(length, random.choice((self.color, other.color)))
            logging.info(f"Created new square with side length: {length}, color: {res.color}")

        return res


def asserts() -> None:
    """
    Asserts of the file.
    :return: None
    """
    temp_rect = Square(len_of_sides=10, color="white")
    assert temp_rect.get_perimeter() == temp_rect.sides * 4
    assert temp_rect.get_area() == temp_rect.sides ** 2

    square_example = Square(0, "red") + Square(0, "blue")
    assert square_example.get_area() == 0.0
    assert square_example.get_perimeter() == 0.0

    square_and_rect_example = Square(10, "red") + Rectangle(10, 20, "blue")
    assert square_and_rect_example.get_area() == 300
    assert square_and_rect_example.get_perimeter() == 100

    rect_and_square_example = Rectangle(10, 20, "blue") + Square(10, "red")
    assert rect_and_square_example.get_area() == 300
    assert rect_and_square_example.get_perimeter() == 100
