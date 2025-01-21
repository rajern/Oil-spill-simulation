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
def test_line_neighbors_two():
    line1 = Line(0, [0, 1], 0)
    line2 = Line(1, [1, 2], 1)
    line3 = Line(2, [2, 3], 2)
    
    # Simulate neighbor checking
    line2.store_neighbors([line2, line3, line1])
    assert line2._neighbors == [2, 0] or [0, 2]



# Testing the Triangle class
def test_triangle_neighbors():
    triangle1 = Triangle(0, [0, 1, 2], 0)
    triangle2 = Triangle(1, [1, 2, 3], 1)

    triangle1.store_neighbors([triangle1, triangle2])
    assert triangle1._neighbors == [{1: [1, 2]}]  # Triangle1 shares points 1 and 2 with Triangle2



# Testing the Mesh class
def test_mesh_creation():
    """Test if mesh creation is working properly."""
    sample_points = [
        [0, 0],  # point 0
        [1, 0],  # point 1
        [1, 1],  # point 2
        [0, 1],  # point 3
        [0.5, 0.5]  # point 4 (middle point)
    ]
    sample_cells = [
        {'type': 'line', 'data': [[0, 1]]},
        {'type': 'triangle', 'data': [[0, 1, 2]]},
        {'type': 'line', 'data': [[2, 3]]},
        {'type': 'triangle', 'data': [[1, 2, 3]]}
    ]
    
    sample_msh = meshio.Mesh(
        points=sample_points,
        cells=sample_cells
    )
    
    mesh = Mesh(sample_msh)
    
    assert len(mesh._points) == 5, f"Expected 5 points, got {len(mesh._points)}"
    assert len(mesh._cells) == 4, f"Expected 4 cells, got {len(mesh._cells)}"
    assert isinstance(mesh._cells[0], Line), f"Expected Line, got {type(mesh._cells[0])}"
    assert isinstance(mesh._cells[1], Triangle), f"Expected Triangle, got {type(mesh._cells[1])}"
    
    print("test_mesh_creation passed!")


def test_mesh_init():
    # Test the initialization of the Mesh class
    mesh = Mesh(sample_points)
    mesh._points = [Point(sample_points, i) for i in range(len(sample_points))]
    assert len(mesh._points) == 4

def test_create_cells():
    # Test the _create_cells method of the Mesh class
    mesh = Mesh(sample_points)
    mesh._points = [Point(sample_points, i) for i in range(len(sample_points))]
    mesh_cells = [[0, 1], [1, 2], [2, 3]]
    cells = mesh._create_cells(mesh_cells)
    assert len(cells) == 3

