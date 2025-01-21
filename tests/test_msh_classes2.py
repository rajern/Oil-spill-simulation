import pytest
import meshio
from packages.simulation.msh_classes import *

# Sample data for points 
@pytest.fixture
def sample_points():
    return [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.5, 0.5]]

# Sample data for cells
@pytest.fixture
def sample_cells():
    return [
        {"type": "line", "data": [[0, 1], [1, 3], [3, 2], [2, 0]]},
        {"type": "triangle", "data": [[0, 1, 4], [1, 3, 4], [3, 2, 4], [2, 0, 4]]},
    ]

@pytest.fixture
def sample_mesh(sample_points, sample_cells):
    class SampleMesh:
        def __init__(self, points, cells):
            self.points = points
            self.cells = [meshio.CellBlock(cell["type"], cell["data"]) for cell in cells]

    return SampleMesh(sample_points, sample_cells)

# Test Point __init__
def test_point_init(sample_points):
    point = Point(sample_points, 0)
    assert point._point_index == 0
    assert point._x == 0.0
    assert point._y == 0.0
    assert repr(point) == "Point(index=0, x=0.00, y=0.00)"

# Test Cell Factory
def test_cell_factory():
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    triangle_cell = Cell.cell_factory("triangle", 1, [0, 1, 2], 1)
    
    assert isinstance(line_cell, Line)
    assert isinstance(triangle_cell, Triangle)
    with pytest.raises(ValueError, match="Unknown cell type"):
        Cell.cell_factory("hexagon", 2, [0, 1, 2, 3], 2)

# Test Line neighbor finding
def test_line_neighbors(sample_points):
    line1 = Line(0, [0, 1], 0)
    line2 = Line(1, [1, 2], 1)
    line3 = Line(2, [2, 3], 2)
    line4 = Line(3, [3, 0], 3)

    lines = [line1, line2, line3, line4]
    for line in lines:
        line.store_neighbors(lines)

    assert line1._neighbors == [1, 3]
    assert line2._neighbors == [0, 2]
    assert line3._neighbors == [1, 3]
    assert line4._neighbors == [0, 2]

# Test Triangle neighbor finding
def test_triangle_neighbors(sample_points):
    triangle1 = Triangle(0, [0, 1, 4], 0)
    triangle2 = Triangle(1, [1, 3, 4], 1)
    triangle3 = Triangle(2, [3, 2, 4], 2)
    triangle4 = Triangle(3, [2, 0, 4], 3)

    triangles = [triangle1, triangle2, triangle3, triangle4]
    for triangle in triangles:
        triangle.store_neighbors(triangles)

    expected_neighbors = [{1: [1, 4]}, {3: [0, 4]}]
    assert triangle1._neighbors == expected_neighbors
    assert len(triangle1._neighbors) == 2

# Test Mesh initialization
def test_mesh_initialization(sample_mesh):
    mesh = Mesh(sample_mesh)
    assert len(mesh._points) == len(sample_mesh.points)
    assert len(mesh._cells) == sum(len(cell.data) for cell in sample_mesh.cells)

# Test Mesh storing coordinates
def test_mesh_store_coordinates(sample_mesh):
    mesh = Mesh(sample_mesh)
    mesh.store_coordinates()

    for cell in mesh._cells:
        assert len(cell._coordinates) == len(cell._cell_points_id)

# Test Mesh finding neighbors
def test_mesh_find_neighbors(sample_mesh):
    mesh = Mesh(sample_mesh)
    mesh.find_neighbors()

    for cell in mesh._cells:
        assert cell._neighbors is not None
