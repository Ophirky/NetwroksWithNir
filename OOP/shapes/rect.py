"""
    Author: Ophir Nevo Michrowski
    DATE: 07/06/2024
    DESCRIPTION: Holds the Rectangle class
"""
from shapes.shape import Shape
import math
import logging
import random


class Rectangle(Shape):
    """Rectangle Class"""

    def __init__(self, width: float, height: float, color: str) -> None:
        """
        Initializer of the rect class
        :param width: The length of the top and bottom sides.
        :param height: The length of the left and right sides.
        :param color: The color of the rectangle.
        """
        super().__init__(color)
        self.width = width
        self.height = height
        logging.info(f"Rectangle created with width: {width}, height: {height}, and color: {color}")

    def get_area(self) -> float:
        """
        Returns the area of the rectangle
        :return float: the area of the rectangle.
        """
        area = self.width * self.height
        logging.debug(f"Calculated area of rectangle (width: {self.width}, height: {self.height}): {area}")
        return area

    def get_perimeter(self) -> float:
        """
        Returns the perimeter of the rectangle
        :return float: perimeter of rectangle
        """
        perimeter = (self.width + self.height) * 2
        logging.debug(f"Calculated perimeter of rectangle (width: {self.width}, height: {self.height}): {perimeter}")
        return perimeter

    @staticmethod
    def _find_rectangle_dimensions(area: float, perimeter: float) -> tuple[float, float]:
        """
        This function will find the length of the sides for the new rectangle
        :param area: The sum of the areas of the two shapes.
        :param perimeter: The sum of the perimeters of the two shapes.
        :return tuple: the lengths of the sides of the new shape.
        """
        # Testing if perimeter and area are valid
        if perimeter < 0 or area < 0:
            logging.debug("Invalid value given.")
            raise ValueError("Perimeter and area must be positive values.")
        elif perimeter == 0 and area == 0:
            return 0.0, 0.0

        # Calculations
        semi_perimeter = perimeter / 2
        discriminant = (-semi_perimeter) ** 2 - 4 * area

        # Testing to see if there is an answer
        if discriminant < 0:
            raise ValueError("No real solutions for the given area and perimeter.")

        # finding the lengths of the sides
        width = (semi_perimeter + math.sqrt(discriminant)) / 2
        length = semi_perimeter - width

        logging.debug(f"Calculated dimensions for area: {area}, perimeter: {perimeter} -> width: {width}, length: {length}")
        return width, length

    def __add__(self, other: Shape) -> Shape:
        """
        Function to handle addition of two shapes.
        :param other: shape that is either a Square or Rectangle.
        :return: new Shape that its area and perimeter are equal to the sum of the sum of the area and perimeter
                 of the two added shapes.
        """
        # Inheriting classes will also return True as an instance of Rectangle
        if not isinstance(other, Rectangle):
            raise ValueError("Rectangle can only be added with other Rectangles!")

        width, length = self._find_rectangle_dimensions(self.get_area() + other.get_area(),
                                                        self.get_perimeter() + other.get_perimeter())

        new_rectangle = Rectangle(width, length, random.choice((self.color, other.color)))
        logging.info(f"Created new rectangle with width: {new_rectangle.width}, height: {new_rectangle.height}," +
                     "color: {new_rectangle.color}")

        return new_rectangle

    def __str__(self) -> str:
        """
        Handles the printing of the rectangle.
        :return str: The dimensions of the Rectangle
        """
        return f"{self.width} x {self.height}, {self.color}"


def asserts() -> None:
    """
    Asserts of the file.
    :return: None
    """
    temp_rect = Rectangle(width=10, height=5, color="white")
    temp_rect_perimeter = (temp_rect.width + temp_rect.height) * 2
    assert temp_rect.get_perimeter() == temp_rect_perimeter, \
        f"Expected {temp_rect_perimeter} but got {temp_rect.get_perimeter()}"

    temp_rect_area = temp_rect.width * temp_rect.height
    assert temp_rect.get_area() == temp_rect_area, \
        f"Expected {temp_rect_area} but got {temp_rect.get_area()}"

    rect_example = Rectangle(11, 12, "red") + Rectangle(9, 8, "blue")
    assert rect_example.get_area() == 204
    assert rect_example.get_perimeter() == 80
