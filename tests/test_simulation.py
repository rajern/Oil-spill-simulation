import pytest
import numpy as np
from packages.simulation.simulation import Sim_Cell, Sim_Line, Sim_Triangle, Sim_Mesh, flux
import meshio

"""
Sample input data for testing.
This includes sample points and cell data for creating mock simulations.
"""
sample_points = [(1, 2), (3, 4), (5, 6)]  # 2D mesh points (x, y)
sample_cell_data = [
    {"type": "line", "data": [[0, 1]]},
    {"type": "triangle", "data": [[0, 1, 2]]}
]

"""
Creating Mock helper functions for tests.
These fixtures provide reusable instances of simulation objects.
"""
@pytest.fixture
def sim_line():
    """
    Fixture to create a simulated line element for testing.
    Calculates the midpoint of the line and returns the instance.
    """
    line = Sim_Line(0, [0, 1], 0)
    line._coordinates = [(0, 0), (1, 1)]
    line.midpoint()
    return line

@pytest.fixture
def sim_triangle():
    """
    Fixture to create a simulated triangle element for testing.
    Calculates the midpoint and area of the triangle and returns the instance.
    """
    triangle = Sim_Triangle(0, [0, 1, 2], 0)
    triangle._coordinates = [(0, 0), (1, 0), (0, 1)]
    triangle.midpoint()
    triangle.area()
    return triangle

@pytest.fixture
def sim_mesh():
    """
    Fixture to create a simulated mesh for testing.
    Initializes the mesh, calculates midpoints, areas, normals, and flow vectors.
    Returns the mesh instance.
    """
    points = [
        [0.0, 0.0],
        [1.0, 0.0],
        [0.5, 0.5]
    ]
    cells = [
        ("line", [[0, 1]]),
        ("triangle", [[0, 1, 2]])
    ]
    msh = meshio.Mesh(points=points, cells=[meshio.CellBlock(type, data) for type, data in cells])
    sim_mesh = Sim_Mesh(msh)
    sim_mesh.store_coordinates()
    sim_mesh.store_midpoint()
    sim_mesh.store_area()
    sim_mesh.normal()
    sim_mesh.flow_vector()
    return sim_mesh


# Testing the flux function.
def test_flux_positive_normal():
    """
    Test that the flux function calculates correctly when the normal vector is positive.
    """
    u_i, u_ngh = 10, 5
    normal, v = np.array([1, 0]), np.array([1, 0])
    flux_value = flux(u_i, u_ngh, normal, v)
    assert flux_value == 10, f"Expected flux: 10, but got: {flux_value}"

def test_flux_negative_normal():
    """
    Test that the flux function calculates correctly when the normal vector is negative.
    """
    u_i, u_ngh = 10, 5
    normal, v = np.array([1, 0]), np.array([-1, 0])
    flux_value = flux(u_i, u_ngh, normal, v)
    assert flux_value == -5, f"Expected flux: -5, but got: {flux_value}"


# Test for class Sim_Cell.
def test_sim_cell():
    """
    Test that the Sim_Cell factory method correctly creates a Sim_Line object when given "line" type.
    """
    cell = Sim_Cell.cell_factory("line", 0, [0, 1], 0)
    assert isinstance(cell, Sim_Line), "Sim_Cell factory did not return a Sim_Line object"


# Tests for class Sim_Line.
def test_sim_line_midpoint(sim_line):
    """
    Test that the midpoint of a simulated line is calculated correctly.
    """
    assert sim_line._midpoint == [0.5, 0.5], f"Expected midpoint: [0.5, 0.5], but got: {sim_line._midpoint}"

def test_sim_line_velocity(sim_line):
    """
    Test that the velocity of a simulated line is calculated correctly.
    """
    sim_line.v()
    expected_velocity = [0.5 - 0.2 * 0.5, -0.5]
    assert np.allclose(sim_line._v, expected_velocity), f"Expected velocity: {expected_velocity}, but got: {sim_line._v}"


# Tests for Sim_Triangle.
def test_sim_triangle_area(sim_triangle):
    """
    Test that the area of a simulated triangle is calculated correctly.
    """
    expected_area = 0.5
    assert sim_triangle._area == expected_area, f"Expected area: {expected_area}, but got: {sim_triangle._area}"

def test_sim_triangle_midpoint(sim_triangle):
    """
    Test that the midpoint of a simulated triangle is calculated correctly.
    """
    expected_midpoint = [1 / 3, 1 / 3]
    assert np.allclose(sim_triangle._midpoint, expected_midpoint), f"Expected midpoint: {expected_midpoint}, but got: {sim_triangle._midpoint}"

def test_sim_triangle_initial_oil(sim_triangle):
    """
    Test that the initial oil concentration of a simulated triangle is calculated correctly.
    """
    x, y = 0.1, 0.1
    sim_triangle.u_0(x, y)
    expected_u = np.exp(-((1 / 3 - x)**2 + (1 / 3 - y)**2) / 0.01)
    assert np.isclose(sim_triangle._u, expected_u), f"Expected oil amount: {expected_u}, but got: {sim_triangle._u}"


# Tests for Sim_Mesh.
def test_sim_mesh_initialization(sim_mesh):
    """
    Test that a simulated mesh is initialized correctly with points and cells.
    """
    assert len(sim_mesh._points) == 3, f"Expected 3 points, but got {len(sim_mesh._points)}"
    assert len(sim_mesh._cells) == 2, f"Expected 2 cells, but got {len(sim_mesh._cells)}"

def test_sim_mesh_area(sim_mesh):
    """
    Test that the areas of cells in the simulated mesh are calculated correctly.
    """
    for cell in sim_mesh._cells:
        if isinstance(cell, Sim_Triangle):
            assert cell._area > 0, f"Expected positive area, but got {cell._area}"

def test_sim_mesh_midpoint(sim_mesh):
    """
    Test that the midpoints of cells in the simulated mesh are calculated correctly.
    """
    for cell in sim_mesh._cells:
        assert cell._midpoint is not None, "Midpoint not calculated"

def test_sim_mesh_initial_oil(sim_mesh):
    """
    Test that the initial oil concentration in the simulated mesh is calculated correctly.
    """
    sim_mesh.initial_oil(0.1, 0.1)
    for cell in sim_mesh._cells:
        if isinstance(cell, Sim_Triangle):
            assert cell._u > 0, "Initial oil value not calculated"

def test_sim_mesh_cells_inside_area(sim_mesh):
    """
    Test that the simulated mesh correctly identifies cells inside a given area.
    """
    area = [[0.0, 1.0], [0.0, 1.0]]
    sim_mesh.cells_inside_area(area)
    assert len(sim_mesh._points_inside_area) > 0, "No cells found inside the area"