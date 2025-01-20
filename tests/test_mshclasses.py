import pytest
from packages.simulation.msh_classes import Point, Cell, Line, Triangle, Mesh

# Testing the Point class
sample_points = [(1, 2), (2, 3), (3, 4), (4, 5)]  # This simulates mesh points
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
    assert repr_str == "Point(index=0, x=1.00, y=2.00)"  

#code from lecture: chech if you are detecting errors correctly
@pytest.mark.parametrize( " input1 , input2 ",
                              [(1 , 0) ,
                               (2 , 0) ,
                               (3.1 , 0) ])
def testDivision(input1 , input2 ):
    with pytest.raises(ZeroDivisionError) as excinfo :
        a = input1 / input2
        assert str( excinfo . value) == " division by zero "

# Testing the Cell class
def test_cell_factory():
    # Create line and triangle cells using the factory
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    triangle_cell = Cell.cell_factory("triangle", 1, [1, 2, 3], 1)

    assert isinstance(line_cell, Line)
    assert isinstance(triangle_cell, Triangle)

def test_point_coord():
    # Test the point_coord method of the Cell class
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    mesh_points = [Point(sample_points, 0), Point(sample_points, 1)]
    x, y = line_cell.point_coord(0, mesh_points)
    assert x == 1
    assert y == 2

def test_get_point_coord():
    # Test the get_point_coord method of the Cell class
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    mesh_points = [Point(sample_points, 0), Point(sample_points, 1)]
    line_cell.get_point_coord(mesh_points)
    assert line_cell._coordinates == [(1, 2), (2, 3)]

# Testing the Line class

def test_line_neighbors():
    line1 = Line(0, [0, 1], 0)
    line2 = Line(1, [1, 2], 1)
    line3 = Line(2, [2, 3], 2)
    
    # Simulate neighbor checking
    line1.store_neighbors([line1, line2, line3])
    assert line1._neighbors == [1]  # Line1 is neighbors with Line2
    #assert line1._is_boundary is True


# def test_line_str():
#     line = Line(0, [0, 1], 0)
#     str_output = str(line)
#     assert str_output == "Line 0: [0, 1]"


# Testing the Triangle class
def test_triangle_neighbors():
    triangle1 = Triangle(0, [0, 1, 2], 0)
    triangle2 = Triangle(1, [1, 2, 3], 1)

    triangle1.store_neighbors([triangle1, triangle2])
    assert triangle1._neighbors == [{1: [1, 2]}]  # Triangle1 shares points 1 and 2 with Triangle2

# def test_triangle_str():
#     triangle = Triangle(0, [0, 1, 2], 0)
#     str_output = str(triangle)
#     assert str_output == "Triangle 0: [0, 1, 2]"


# Testing the Mesh class

def test_mesh_init():
    # Test the initialization of the Mesh class
    mesh = Mesh(sample_points)
    assert len(mesh._points) == 4

