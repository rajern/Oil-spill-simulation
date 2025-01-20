import pytest
from packages.simulation.msh_classes import Point

# Sample mesh data for testing

sample_points = [(1, 2), (3, 4), (5, 6)]  # This simulates mesh points, where each tuple is (x, y)

def test_point_x():
    # Test the x property of the Point class
    point = Point(sample_points, 0)
    assert point._x == 1

def test_point_y():
    # Test the y property of the Point class
    point = Point(sample_points, 0)
    assert point._y == 2

def test_point_index():
    # Test the point_index property of the Point class
    point = Point(sample_points, 0)
    assert point._point_index == 0


def test_point_repr():
    point = Point(sample_points, 0)
    repr_str = repr(point)
    assert repr_str == "Point(index=0, x=1.00, y=2.00)"  # Only one assertion since it's about the representation


# def test_edge_case_empty_mesh():
#     # Test the behavior when the mesh has no points
#     empty_points = []
#     with pytest.raises(IndexError):  # IndexError because no points to access
#         point = Point(empty_points, 0)

# def test_point_index_out_of_range():
#     # Test if accessing an out-of-range index causes an error
#     out_of_range_index = 10
#     with pytest.raises(IndexError):  # IndexError because index 10 does not exist in the mesh
#         point = Point(sample_points, out_of_range_index)

# def test_mesh_point_access():
#     # Test to ensure that the Mesh class correctly initializes Point objects
#     class Mesh:
#         def __init__(self, msh):
#             '''input: mesh
#             reads in points and cells into lists that store metadata'''
#             self._points = [Point(msh, i) for i in range(len(msh))]

#     mesh = Mesh(sample_points)
#     # Check that we correctly have a list of Point objects
#     assert isinstance(mesh._points[0], Point)
#     assert mesh._points[0]._x == 1
#     assert mesh._points[0]._y == 2
#     assert mesh._points[1]._x == 3
#     assert mesh._points[1]._y == 4

