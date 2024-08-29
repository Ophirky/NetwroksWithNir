"""
    Author: Ophir Nevo Michrowski
    DATE: 07/06/2024
    DESCRIPTION: Holds the Circle class
"""
import math
import logging

from shapes.shape import Shape


class Circle(Shape):
    """Circle Class"""

    def __init__(self, radius: float, color: str) -> None:
        """
        Initializer of the Circle class
        :param radius: The radius of the circle.
        :param color: The color of the circle.
        """
        super().__init__(color)
        self.radius = radius
        logging.info(f"Circle created with radius: {radius} and color: {color}")

    def get_area(self) -> float:
        """
        Returns the area of the circle
        :return float: The area of the circle.
        """
        area = math.pi * self.radius ** 2
        logging.debug(f"Calculated area of circle with radius {self.radius}: {area}")
        return area

    def get_perimeter(self) -> float:
        """
        Returns the perimeter of the circle
        :return float: perimeter of circle
        """
        perimeter = 2 * math.pi * self.radius
        logging.debug(f"Calculated perimeter of circle with radius {self.radius}: {perimeter}")
        return perimeter


def asserts() -> None:
    """
    Asserts of the file.
    :return: None
    """
    temp_rect = Circle(radius=10, color="white")
    assert temp_rect.get_area() == math.pi * temp_rect.radius ** 2
    assert temp_rect.get_perimeter() == 2 * math.pi * temp_rect.radius
