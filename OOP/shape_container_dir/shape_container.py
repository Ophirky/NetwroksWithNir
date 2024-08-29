"""
    AUTHOR: Ophir nevo Michrowski.
    DATE: 29/08/2024.
    DESCRIPTION: Containing the ShapeContainer class.
"""
import random
import logging
from shape_container_dir.shape_types import ShapeTypes
from shape_container_dir.colors import Colors

MAX_SIDE_LENGTH = 10
MIN_SIDE_LENGTH = 1


class ShapeContainer:
    """This is the Shape Container class - Stores a tuple of shapes."""

    def __init__(self) -> None:
        """
        Initializer of ShapeContainer
        """
        self.__shapes: tuple = tuple()
        self.__sorted_by_color: dict[Colors, int] = dict()
        logging.info("ShapeContainer initialized")

    def generate(self, amount: int) -> None:
        """
        Will generate a tuple of x shapes according to the given amount.
        :param amount: The amount of shapes to generate.
        :return: None
        """
        shapes = list()

        for i in range(amount):
            # Generating parameters for shape
            shape = random.choice(tuple(ShapeTypes))
            side_length = random.randint(MIN_SIDE_LENGTH, MAX_SIDE_LENGTH)
            color = random.choice(tuple(Colors)).value

            # finding the right shape
            match shape:
                case ShapeTypes.RECT:
                    new_side = random.randint(MIN_SIDE_LENGTH, MAX_SIDE_LENGTH)
                    shape = shape.value(new_side, side_length, color)
                    shapes.append(shape)

                case _:
                    shape = shape.value(side_length, color)
                    shapes.append(shape)

            logging.debug(f"Generated shape: {shape} (side length: {side_length}, color: {color})")

            # Organizing by color
            self.__sorted_by_color[color] = self.__sorted_by_color.get(color, 0) + 1

        # putting in the shape container
        self.__shapes = tuple(shapes)

    def sum_areas(self) -> float:
        """
        Sums all the areas of all the shapes in the container.
        :return float: sum of areas.
        """
        sum_of_areas = 0
        for i in self.__shapes:
            sum_of_areas += i.get_area()

        logging.debug(f"Total area: {sum_of_areas}")

        return sum_of_areas

    def sum_perimeters(self) -> float:
        """
        Sums all the perimeters of all the shapes in the container.
        :return float: sum of perimeters.
        """
        sum_of_perimeter = 0
        for i in self.__shapes:
            sum_of_perimeter += i.get_perimeter()

        logging.debug(f"Total perimeter: {sum_of_perimeter}")

        return sum_of_perimeter

    def count_colors(self):
        """
        counts colors in __shapes
        :return dict[Color, int]: {Color: amount_of_shapes_with_that_color}
        """
        logging.debug(f"Color count: {self.__sorted_by_color}")
        return self.__sorted_by_color


def asserts() -> None:
    """
    Automatic tests for file.
    :return: None
    """
    shape_amount = 10
    shape = ShapeContainer()
    shape.generate(shape_amount)

    assert sum(shape.count_colors().values()) == shape_amount
    assert shape.sum_areas() > 0
    assert shape.sum_perimeters() > 0
