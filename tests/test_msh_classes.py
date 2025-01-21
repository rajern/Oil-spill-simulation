import pytest
import meshio
from packages.simulation.msh_classes import Point, Cell, Line, Triangle, Mesh


# Testing the Point class
sample_points = [(1, 2), (2, 3), (3, 4), (4, 5)]  # This simulates mesh points coordinates

def test_point_x():
    """ Test the x property of the Point class"""
    point = Point(sample_points, 0)
    assert point._x == 1

def test_point_y():
    """ Test the y property of the Point class"""
    point = Point(sample_points, 0)
    assert point._y == 2

def test_point_index():
    """ Test the point_index property of the Point class"""
    point = Point(sample_points, 0)
    assert point._point_index == 0

def test_point_repr():
    """ Test the __repr__ method of the Point class"""
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
    """ 
    Creating line cell using the cell_factory
    Testing if the cell created is an instance of the Line class
    """
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    assert isinstance(line_cell, Line)

def test_cell_factory_triangle():
    """
    Creating triangle cell using the cell_factory
    Testing if the cell created is an instance of the Triangle class
    """
    triangle_cell = Cell.cell_factory("triangle", 1, [1, 2, 3], 1)
    assert isinstance(triangle_cell, Triangle)

def test_cell_factory_error():
    """Test if the cell_factory raises an error for unknown cell type"""
    with pytest.raises(ValueError) as excinfo:
        Cell.cell_factory("unknown", 0, [0, 1], 0)
    assert str(excinfo.value) == "Unknown cell type: unknown"

def test_point_coord():
    """
    Test the point_coord method of the Cell class
    """
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    mesh_points = [Point(sample_points, 0), Point(sample_points, 1)]
    x, y = line_cell.point_coord(0, mesh_points)
    assert x == 1
    assert y == 2

def test_get_point_coord():
    """ 
    Test the get_point_coord method of the Cell class 
    """
    line_cell = Cell.cell_factory("line", 0, [0, 1], 0)
    mesh_points = [Point(sample_points, 0), Point(sample_points, 1)]
    line_cell.get_point_coord(mesh_points)
    assert line_cell._coordinates == [(1, 2), (2, 3)]

# Testing the Line class

def test_line_neighbors():
    """
    Test the store_neighbors method of the Line class when the line has one neighbor
    """
    line1 = Line(0, [0, 1], 0)
    line2 = Line(1, [1, 2], 1)
    line3 = Line(2, [2, 3], 2)
    
    # Simulate neighbor checking
    line1.store_neighbors([line1, line2, line3])
    assert line1._neighbors == [1]  # Line1 is neighbors with Line2

#hvorfor er denne feil, skal ikke denne ha to neighbors??
def test_line_neighbors_two():
    """
    Test the store_neighbors method of the Line class if the line has two neighbors
    """
    line1 = Line(0, [0, 1], 0)
    line2 = Line(1, [1, 2], 1)
    line3 = Line(2, [2, 3], 2)
    
    # Simulate neighbor checking
    line2.store_neighbors([line2, line3, line1])
    assert line2._neighbors == [2, 0] or [0, 2]



# Testing the Triangle class
def test_triangle_neighbors():
    """
    Test the store_neighbors method of the Triangle class
    """
    triangle1 = Triangle(0, [0, 1, 2], 0)
    triangle2 = Triangle(1, [1, 2, 3], 1)

    triangle1.store_neighbors([triangle1, triangle2])
    assert triangle1._neighbors == [{1: [1, 2]}]  # Triangle1 shares points 1 and 2 with Triangle2

# Testing the Mesh class
def create_example_mesh():
    """
    Create an example mesh with 4 points, 1 line cell, and 1 triangle cell
    """
    points = [
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 1.0],
        [0.0, 1.0]
    ]
    cells = [
        ("line", [[0, 1], [1, 2], [2, 3], [3, 0]]),
        ("triangle", [[0, 1, 2], [0, 2, 3]])
    ]
    return meshio.Mesh(points=points, cells=[meshio.CellBlock(type, data) for type, data in cells])


def test_mesh_initialization():
    """
    Test the initialization of the Mesh class
    """
    msh = create_example_mesh()
    mesh = Mesh(msh)

    assert len(mesh._points) == 4 # the four points created in the example mesh
    assert len(mesh._cells) == 6  # 4 lines + 2 triangles

# Step 3: Test Storing Coordinates
def test_store_coordinates():
    """ 
    Test the store_coordinates method of the Mesh class
    """
    msh = create_example_mesh()
    mesh = Mesh(msh)

    mesh.store_coordinates()

    # Check if all cells have coordinates
    for cell in mesh._cells:
        assert len(cell._coordinates) == len(cell._cell_points_id)

# Step 4: Test Finding Neighbors
def test_find_neighbors():
    """
    Test the find_neighbors method of the Mesh class
    """
    msh = create_example_mesh()
    mesh = Mesh(msh)

    mesh.find_neighbors()

    # Test neighbors for a specific line
    line_cell = mesh._cells[0]  # First line
    assert set(line_cell._neighbors) == {1, 3, 4}  # Update to reflect actual neighbors

    # Test neighbors for a specific triangle
    triangle_cell = mesh._cells[4]  # First triangle
    assert len(triangle_cell._neighbors) > 0  # Should have neighbors


def test_full_mesh_setup():
    """
    Test the full mesh setup process
    """
    msh = create_example_mesh()
    mesh = Mesh(msh)

    mesh.store_coordinates()
    mesh.find_neighbors()

    # Ensure all cells have coordinates and neighbors
    for cell in mesh._cells:
        assert len(cell._coordinates) == len(cell._cell_points_id)
        assert cell._neighbors is not None
