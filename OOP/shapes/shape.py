"""
    Author: Ophir Nevo Michrowski
    DATE: 07/06/2024
    DESCRIPTION: Abstract class - shape
"""
import logging
from abc import ABC, abstractmethod


class Shape(ABC):
    """This is an abstract class - shape"""

    def __init__(self, color: str) -> None:
        """
        Initializer of the abstract class Shape
        :param color: The color of the shape
        """
        self.__color = color
        logging.info("log")

    @property
    def color(self) -> str:
        """
        Defining the property "color" and getter for the color property
        :return str: The color
        """
        return self.__color

    @color.setter
    def color(self, value: str) -> None:
        """
        Setter for the color property.
        :param value: The new color.
        :return: None
        """
        self.__color = value

    @abstractmethod
    def get_area(self) -> float:
        """
        Returns the area of the shape
        :return float: the area of the shape.
        """
        pass

    @abstractmethod
    def get_perimeter(self) -> float:
        """
        Returns the perimeter of the shape
        :return float: perimeter of shape
        """
        pass


# implementation for testing
class _TestShapeImpl(Shape):

    def __init__(self):
        super().__init__("red")

    def get_area(self) -> float:
        return 0.0

    def get_perimeter(self) -> float:
        return 0.0


# Automated tests
def asserts():
    shape = _TestShapeImpl()

    # Test initial color
    assert shape.color == "red", f"Expected 'red', but got {shape.color}"

    # Test set_color
    shape.color = "blue"
    assert shape.color == "blue", f"Expected 'blue', but got {shape.color}"

    # Test get_area
    assert shape.get_area() == 0.0, f"Expected 0.0, but got {shape.get_area()}"

    # Test get_perimeter
    assert shape.get_perimeter() == 0.0, f"Expected 0.0, but got {shape.get_perimeter()}"
