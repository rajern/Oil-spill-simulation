import pytest
import numpy as np
from packages.simulation.simulation import Sim_Cell, Sim_Line, Sim_Triangle, Sim_Mesh, flux

# Sample input data
sample_points = [(1, 2), (3, 4), (5, 6)]  # 2D mesh points (x, y)
sample_cell_data = [
    {"type": "line", "data": [[0, 1]]},
    {"type": "triangle", "data": [[0, 1, 2]]}
]  # Mock cell data with line and triangle cells

@pytest.fixture
def sim_mesh():
    # Creating a Sim_Mesh object using mock data
    mesh = Sim_Mesh(sample_cell_data)
    mesh.store_area()  # Calculate areas
    mesh.store_midpoint()  # Calculate midpoints
    return mesh

@pytest.fixture
def sim_triangle():
    # Mocking a Sim_Triangle object with 3 points
    triangle = Sim_Triangle(0, [0, 1, 2], 0)
    triangle._coordinates = [(0, 0), (1, 0), (0, 1)]
    triangle.midpoint()  # Calculate the midpoint of the triangle
    triangle.area()  # Calculate the area of the triangle
    return triangle

@pytest.fixture
def sim_line():
    # Mocking a Sim_Line object with 2 points
    line = Sim_Line(0, [0, 1], 0)
    line._coordinates = [(0, 0), (1, 1)]
    line.midpoint()  # Calculate the midpoint of the line
    return line
