"""
Functions used to support drawing. No Pyglet/OpenGL here.
"""

import math

from typing import List, Tuple, cast

from arcade import Color
from arcade import RGBA


def get_points_for_thick_line(start_x: float, start_y: float,
                              end_x: float, end_y: float,
                              line_width: float):
    """
    Function used internally for Arcade. OpenGL draws triangles only, so a think
    line must be two triangles that make up a rectangle. This calculates those
    points.
    """
    vector_x = start_x - end_x
    vector_y = start_y - end_y
    perpendicular_x = vector_y
    perpendicular_y = -vector_x
    length = math.sqrt(vector_x * vector_x + vector_y * vector_y)
    if length == 0:
        normal_x = 1.0
        normal_y = 1.0
    else:
        normal_x = perpendicular_x / length
        normal_y = perpendicular_y / length
    r1_x = start_x + normal_x * line_width / 2
    r1_y = start_y + normal_y * line_width / 2
    r2_x = start_x - normal_x * line_width / 2
    r2_y = start_y - normal_y * line_width / 2
    r3_x = end_x + normal_x * line_width / 2
    r3_y = end_y + normal_y * line_width / 2
    r4_x = end_x - normal_x * line_width / 2
    r4_y = end_y - normal_y * line_width / 2
    points = (r1_x, r1_y), (r2_x, r2_y), (r4_x, r4_y), (r3_x, r3_y)
    return points


def get_four_byte_color(color: Color) -> RGBA:
    """
    Given a RGB list, it will return RGBA.
    Given a RGBA list, it will return the same RGBA.

    :param Color color: Three or four byte tuple

    :returns:  return: Four byte RGBA tuple
    """

    if len(color) == 4:
        return cast(RGBA, color)
    elif len(color) == 3:
        return color[0], color[1], color[2], 255
    else:
        raise ValueError("This isn't a 3 or 4 byte color")


def get_four_float_color(color: Color) -> Tuple[float, float, float, float]:
    """
    Given a 3 or 4 RGB/RGBA color where each color goes 0-255, this
    returns a RGBA tuple where each item is a scaled float from 0 to 1.

    :param Color color: Three or four byte tuple
    :return: Four floats as a RGBA tuple
    """
    if len(color) == 4:
        return color[0] / 255, color[1] / 255, color[2] / 255, color[3] / 255  # type: ignore
    elif len(color) == 3:
        return color[0] / 255, color[1] / 255, color[2] / 255, 1.0
    else:
        raise ValueError("This isn't a 3 or 4 byte color")


def make_transparent_color(color: Color, transparency: float):
    """
    Given a RGB color, along with an alpha, returns a RGBA color tuple.

    :param Color color: Three or four byte RGBA color
    :param float transparency: Transparency
    """
    return color[0], color[1], color[2], transparency


def rotate_point(x: float, y: float, cx: float, cy: float,
                 angle_degrees: float) -> List[float]:
    """
    Rotate a point around a center.

    :param x: x value of the point you want to rotate
    :param y: y value of the point you want to rotate
    :param cx: x value of the center point you want to rotate around
    :param cy: y value of the center point you want to rotate around
    :param angle_degrees: Angle, in degrees, to rotate
    :return: Return rotated (x, y) pair
    :rtype: (float, float)
    """
    temp_x = x - cx
    temp_y = y - cy

    # now apply rotation
    angle_radians = math.radians(angle_degrees)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    rotated_x = temp_x * cos_angle - temp_y * sin_angle
    rotated_y = temp_x * sin_angle + temp_y * cos_angle

    # translate back
    rounding_precision = 2
    x = round(rotated_x + cx, rounding_precision)
    y = round(rotated_y + cy, rounding_precision)

    return [x, y]
