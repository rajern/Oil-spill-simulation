import pytest
import meshio
from packages.simulation.msh_classes import Point, Cell, Line, Triangle, Mesh
# får ikke til å teste mesh classen her.. 
# og må velge om man skal starte med å sette fixtures som nedereste del av koden gjør.


@pytest.fixture
def sample_points():
    return [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.5, 0.5]]

@pytest.fixture
def sample_cells():
    return [
        {"type": "line", "data": [[0, 1], [1, 3], [3, 2], [2, 0]]},
        {"type": "triangle", "data": [[0, 1, 4], [1, 3, 4], [3, 2, 4], [2, 0, 4]]},
    ]

@pytest.fixture
def mock_mesh(sample_points, sample_cells):
    class MockMesh:
        def __init__(self, points, cells):
            self.points = points
            self.cells = [meshio.CellBlock(cell["type"], cell["data"]) for cell in cells]

    return MockMesh(sample_points, sample_cells)

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

def test_line_neighbors_boundary():
    line1 = Line(0, [0, 1], 0)
    line2 = Line(1, [1, 2], 1)
    line3 = Line(2, [2, 3], 2)
    
    # Simulate neighbor checking
    line1.store_neighbors([line1, line2, line3])
    assert line1._is_boundary is True

# Testing the Triangle class
def test_triangle_neighbors():
    triangle1 = Triangle(0, [0, 1, 2], 0)
    triangle2 = Triangle(1, [1, 2, 3], 1)

    triangle1.store_neighbors([triangle1, triangle2])
    assert triangle1._neighbors == [{1: [1, 2]}]  # Triangle1 shares points 1 and 2 with Triangle2
