from intersect_coordinator import *


def test_should_assert_that_point_lies_on_segment():
    p = (0, 0)
    r = (0, 5)
    q = (0, 1)
    assert on_segment(p, q, r)


def test_should_assert_that_point_do_not_lies_on_segment():
    p = (0, 0)
    r = (0, 5)
    q = (-1, 0)
    assert not on_segment(p, q, r)


def test_should_assert_that_points_are_clockwise_arranged():
    p = (0, 0)
    q = (1, 1)
    r = (2, 0)
    assert 1 == orientation(p, q, r)


def test_should_assert_that_points_are_counterclockwise_arranged():
    p = (1, 1)
    q = (0, 0)
    r = (2, 0)
    assert 2 == orientation(p, q, r)


def test_should_assert_that_segments_intersect():
    p1 = (1, 0)
    q1 = (1, 1)
    p2 = (0, 1)
    q2 = (3, 1)
    assert do_intersect(p1, q1, p2, q2)


def test_should_assert_that_point_is_inside_rectangle():
    polygon = [(0, 0), (0, 5), (5, 5), (5, 0)]
    point = (3, 3)
    assert is_inside_polygon(polygon, point)
