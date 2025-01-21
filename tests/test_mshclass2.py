
#!!!!!!!!USING FIXTURES!!!!!!!!!!
import pytest
from packages.simulation.msh_classes import Point, Cell, Line, Triangle, Mesh

# Sample mesh data
sample_points = [(1, 2), (2, 3), (3, 4), (4, 5)]  # This simulates mesh points

# Fixture to create sample points
@pytest.fixture
def sample_points_fixture():
    points = []
    for i in range(len(sample_points)):
        points.append(Point(sample_points, i))
    return points

# Fixture to create a Mesh object with sample points
@pytest.fixture
def mesh_fixture(sample_points_fixture):
    return Mesh(sample_points_fixture)

# Fixture to create a Line cell
@pytest.fixture
def line_cell():
    return Line(0, [0, 1], 0)

# Fixture to create a Triangle cell
@pytest.fixture
def triangle_cell():
    return Triangle(0, [0, 1, 2], 0)

# Test for the Point class
def test_point_x(sample_points_fixture):
    point = sample_points_fixture[0]
    assert point._x == 1

def test_point_y(sample_points_fixture):
    point = sample_points_fixture[0]
    assert point._y == 2

def test_point_index(sample_points_fixture):
    point = sample_points_fixture[0]
    assert point._point_index == 0

def test_point_repr(sample_points_fixture):
    point = sample_points_fixture[0]
    repr_str = repr(point)
    assert repr_str == "Point(index=0, x=1.00, y=2.00)"

# Test for the Cell class
def test_cell_factory():
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    triangle_cell = Cell.cell_factory("triangle", 1, [1, 2, 3], 1)

    assert isinstance(line_cell, Line)
    assert isinstance(triangle_cell, Triangle)

def test_point_coord(line_cell, sample_points_fixture):
    mesh_points = sample_points_fixture
    x, y = line_cell.point_coord(0, mesh_points)
    assert x == 1
    assert y == 2

def test_get_point_coord(line_cell, sample_points_fixture):
    mesh_points = sample_points_fixture
    line_cell.get_point_coord(mesh_points)
    assert line_cell._coordinates == [(1, 2), (2, 3)]

# Test for Line class
def test_line_neighbors(line_cell):
    line2 = Line(1, [1, 2], 1)
    line3 = Line(2, [2, 3], 2)
    line_cell.store_neighbors([line_cell, line2, line3])
    assert line_cell._neighbors == [1]  # Line1 is neighbors with Line2

# def test_line_str(line_cell):
#     str_output = str(line_cell)
#     assert str_output == "Line 0, Boundary: False, Neighbors: [1]"

# Test for Triangle class
def test_triangle_neighbors(triangle_cell):
    triangle2 = Triangle(1, [1, 2, 3], 1)
    triangle_cell.store_neighbors([triangle_cell, triangle2])
    assert triangle_cell._neighbors == [{1: [1, 2]}]  # Triangle1 shares points 1 and 2 with Triangle2

# Test for Mesh class:

def test_mesh_init(mesh_fixture):
    mesh = mesh_fixture
    mesh_points = mesh._points
    assert len(mesh_points) == 4
