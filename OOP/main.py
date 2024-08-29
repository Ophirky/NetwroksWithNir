"""
    Author: Ophir Nevo Michrowski
    DATE: 07/06/2024
    DESCRIPTION: Main program of the exercise.
"""
import shape_container_dir.shape_container
from shape_container_dir.shape_container import ShapeContainer
from shapes import circle, rect, shape, square
import logging
import os

# Constants
LOG_LEVEL = logging.ERROR
LOG_DIR = r"Logs"
LOG_FILE = LOG_DIR + r"\log.log"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"

def asserts() -> None:
    """
    run all the auto tests of the project.
    :return: None
    """
    shape.asserts()
    circle.asserts()
    square.asserts()
    rect.asserts()
    shape_container_dir.shape_container.asserts()


def main() -> None:
    """
    The main function of the project.
    :return: None
    """
    my_container = ShapeContainer()
    my_container.generate(100)
    print("total area:", my_container.sum_areas())
    print("total perimeter:", my_container.sum_perimeters())
    print("colors:", my_container.count_colors())


if __name__ == '__main__':
    # Run asserts
    asserts()

    # Setup Logger
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Log setup
    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename=LOG_FILE, mode='a')
    formatter = logging.Formatter(LOG_FORMAT)
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(LOG_LEVEL)

    # Running the main function
    main()
