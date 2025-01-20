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


# #code from lecture: chech if you are detecting errors correctly
# @pytest.mark.parametrize( " input1 , input2 ",
#                               [(1 , 0) ,
#                                (2 , 0) ,
#                                (3.1 , 0) ])
# def testDivision(input1 , input2 ):
#     with pytest.raises(ZeroDivisionError) as excinfo :
#         a = input1 / input2
#         assert str( excinfo . value) == " division by zero "


# # Sample mesh data for testing
# sample_points = [(0, 0), (1, 0), (0, 1), (1, 1)]  # Four points: (x, y)
# sample_cells = [
#     {"type": "line", "data": [[0, 1], [1, 2]]},  # Two line cells
#     {"type": "triangle", "data": [[0, 1, 2], [1, 2, 3]]},  # Two triangle cells
# ]

# # Fixture for Mesh creation
# @pytest.fixture
# def mesh():
#     return Mesh(sample_cells)


# # Point class tests
# def test_point_initialization():
#     point = Point(sample_points, 0)
#     assert point._point_index == 0
#     assert point._x == 0
#     assert point._y == 0

# def test_point_repr():
#     point = Point(sample_points, 1)
#     repr_str = repr(point)
#     assert repr_str == "Point(index=1, x=1.00, y=0.00)"


# # Testing the Cell class factory
# def test_cell_factory():
#     # Create line and triangle cells using the factory
#     line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
#     triangle_cell = Cell.cell_factory("triangle", 1, [1, 2, 3], 1)

#     assert isinstance(line_cell, Line)
#     assert isinstance(triangle_cell, Triangle)


# # Testing the Line class
# def test_line_neighbors():
#     line1 = Line(0, [0, 1], 0)
#     line2 = Line(1, [1, 2], 1)
#     line3 = Line(2, [2, 3], 2)
    
#     # Simulate neighbor checking
#     line1.store_neighbors([line1, line2, line3])
#     assert line1._neighbors == [1]  # Line1 is neighbors with Line2
#     #assert line1._is_boundary is True


# # Testing the Triangle class
# def test_triangle_neighbors():
#     triangle1 = Triangle(0, [0, 1, 2], 0)
#     triangle2 = Triangle(1, [1, 2, 3], 1)

#     triangle1.store_neighbors([triangle1, triangle2])
#     assert triangle1._neighbors == [{1: [1, 2]}]  # Triangle1 shares points 1 and 2 with Triangle2


# # Testing the Mesh class
# def test_mesh_creation():
#     mesh = Mesh(sample_cells)
#     assert len(mesh._points) == 4  # Four points created
#     assert len(mesh._cells) == 4   # Two line cells and two triangle cells


# def test_store_coordinates():
#     mesh = Mesh(sample_cells)
#     mesh.store_coordinates()

#     # Test that each cell has coordinates
#     for cell in mesh._cells:
#         assert len(cell._coordinates) > 0


# def test_find_neighbors():
#     # Create cells and mesh
#     mesh = Mesh(sample_cells)
    
#     # Store coordinates and neighbors
#     mesh.store_coordinates()
#     mesh.find_neighbors()
    
#     # Test that neighbors are correctly assigned
#     for cell in mesh._cells:
#         if isinstance(cell, Line):
#             assert len(cell._neighbors) > 0  # Line should have neighbors
#         elif isinstance(cell, Triangle):
#             assert len(cell._neighbors) > 0  # Triangle should have neighbors


# # Parametrized tests for Point
# @pytest.mark.parametrize("index, expected_x, expected_y", [
#     (0, 0, 0),
#     (1, 1, 0),
#     (2, 0, 1),
#     (3, 1, 1)
# ])
# def test_point_coordinates(index, expected_x, expected_y):
#     point = Point(sample_points, index)
#     assert point._x == expected_x
#     assert point._y == expected_y


# # Parametrized tests for Cell creation
# @pytest.mark.parametrize("cell_type, expected_class", [
#     ("line", Line),
#     ("triangle", Triangle)
# ])
# def test_cell_factory_parametrized(cell_type, expected_class):
#     cell = Cell.cell_factory(cell_type, 0, [0, 1], 0)
#     assert isinstance(cell, expected_class)


