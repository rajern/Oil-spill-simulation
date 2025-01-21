import pytest
from packages.simulation.msh_classes import Point, Cell, Line, Triangle, Mesh
# får ikke til å teste mesh classen her.. 
# og må velge om man skal starte med å sette fixtures som nedereste del av koden gjør.


# Testing the Point class
sample_points = [(1, 2), (2, 3), (3, 4), (4, 5)]  # This simulates mesh points coordinates

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
def test_cell_factory_line():
    # Creating line cell using the cell_factory
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    assert isinstance(line_cell, Line)

def test_cell_factory_triangle():
    # Creating triangle cell using the cell_factory
    triangle_cell = Cell.cell_factory("triangle", 1, [1, 2, 3], 1)
    assert isinstance(triangle_cell, Triangle)

def test_cell_factory_error():
    # Test for an unknown cell type
    with pytest.raises(ValueError) as excinfo:
        Cell.cell_factory("unknown", 0, [0, 1], 0)
    assert str(excinfo.value) == "Unknown cell type: unknown"

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

#hvorfor er denne feil, skal ikke denne ha to neighbors??
# def test_line_neighbors_two():
#     line1 = Line(0, [0, 1], 0)
#     line2 = Line(1, [1, 2], 1)
#     line3 = Line(2, [2, 3], 2)
    
#     # Simulate neighbor checking
#     line2.store_neighbors([line2, line3, line1])
#     assert line2._neighbors == [2]

def test_line_neighbors_boundary():
    line1 = Line(0, [0, 1], 0)
    line2 = Line(1, [1, 2], 1)
    line3 = Line(2, [2, 3], 2)
    
    # Simulate neighbor checking
    line1.store_neighbors([line1, line2, line3])
    assert line1._is_boundary is True

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

# Sample data for testing
sample_points = [(1, 2), (2, 3), (3, 4), (4, 5)]  # Sample points (x, y)
sample_cells = [
    {"type": "line", "data": [[0, 1]]},  # Line cell connecting points 0 and 1
    {"type": "triangle", "data": [[0, 1, 2]]}  # Triangle cell connecting points 0, 1, and 2
]
# Test Data for parametrize
test_mesh_data = [
    # (points, cells, expected number of points, expected number of cells)
    (sample_points, sample_cells, 4, 2),
]

# Test for the Mesh class initialization
@pytest.mark.parametrize("points, cells, expected_num_points, expected_num_cells", test_mesh_data)
def test_mesh_initialization(points, cells, expected_num_points, expected_num_cells):
    # Create the mesh object
    mesh_data = {"points": points, "cells": cells}
    mesh = Mesh(mesh_data)

    # Assert that the number of points and cells are correct
    assert len(mesh._points) == expected_num_points, f"Expected {expected_num_points} points, but got {len(mesh._points)}"
    assert len(mesh._cells) == expected_num_cells, f"Expected {expected_num_cells} cells, but got {len(mesh._cells)}"

# Test the store_coordinates method
@pytest.mark.parametrize("points, cells", test_mesh_data)
def test_store_coordinates(points, cells):
    # Create the mesh object
    mesh_data = {"points": points, "cells": cells}
    mesh = Mesh(mesh_data)

    # Store coordinates for the cells
    mesh.store_coordinates()

    # Assert that the coordinates for the first cell are correctly stored
    first_cell = mesh._cells[0]
    assert first_cell._coordinates == [(1, 2), (2, 3)], f"Expected coordinates [(1, 2), (2, 3)], but got {first_cell._coordinates}"

    # Assert that the coordinates for the second cell (triangle) are correctly stored
    second_cell = mesh._cells[1]
    assert second_cell._coordinates == [(1, 2), (2, 3), (3, 4)], f"Expected coordinates [(1, 2), (2, 3), (3, 4)], but got {second_cell._coordinates}"

# Test the find_neighbors method
@pytest.mark.parametrize("points, cells", test_mesh_data)
def test_find_neighbors(points, cells):
    # Create the mesh object
    mesh_data = {"points": points, "cells": cells}
    mesh = Mesh(mesh_data)

    # Store coordinates and find neighbors
    mesh.store_coordinates()
    mesh.find_neighbors()

    # Test that the line cell correctly identifies its neighbor (triangle cell)
    line_cell = mesh._cells[0]
    assert line_cell._neighbors == [1], f"Expected neighbors [1] for line cell, but got {line_cell._neighbors}"

    # Test that the triangle cell correctly identifies its neighbors (line cell)
    triangle_cell = mesh._cells[1]
    assert triangle_cell._neighbors == [{0: [0, 1]}], f"Expected neighbors [{0: [0, 1]}] for triangle cell, but got {triangle_cell._neighbors}"




# def test_mesh_init():
#     # Test the initialization of the Mesh class
#     mesh = Mesh(sample_points)
#     mesh._points = [Point(sample_points, i) for i in range(len(sample_points))]
#     assert len(mesh._points) == 4

# def test_create_cells():
#     # Test the _create_cells method of the Mesh class
#     mesh = Mesh(sample_points)
#     mesh._points = [Point(sample_points, i) for i in range(len(sample_points))]
#     mesh_cells = [[0, 1], [1, 2], [2, 3]]
#     cells = mesh._create_cells(mesh_cells)
#     assert len(cells) == 3

