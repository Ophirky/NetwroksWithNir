"""
    AUTHOR: Ophir nevo Michrowski.
    DATE: 29/08/2024.
    DESCRIPTION: Containing All the shape types there are.
"""
from enum import Enum

from shapes import circle, rect, square
from shapes.shape import Shape

class ShapeTypes(Enum):
    """All the shape types in the project"""
    CIRCLE: Shape = circle.Circle
    RECT: Shape = rect.Rectangle
    SQUARE: Shape = square.Square

