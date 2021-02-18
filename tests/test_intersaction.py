from src.intersect_coordinator import *


def test_should_say_that_point_is_inside_rectangle():
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0)]
    point = (3, 3)
    assert is_inside_polygon(polygon, point)
