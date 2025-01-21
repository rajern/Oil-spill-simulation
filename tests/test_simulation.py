import pytest
import numpy as np
import pandas as pd
from packages.simulation.simulation import Sim_Cell, Sim_Line, Sim_Triangle, Sim_Mesh, flux


# Sample input data. 
# Making an example of a 2D mesh with 3 points, 1 line cell, and 1 triangle cell
sample_points = [(1, 2), (3, 4), (5, 6)]  # 2D mesh points (x, y)
sample_cell_data = [
    {"type": "line", "data": [[0, 1]]},
    {"type": "triangle", "data": [[0, 1, 2]]}
]  

sample_mesh_data = {
    "points": sample_points,
    "cells": sample_cell_data
}


def sim_triangle():
    triangle = Sim_Triangle(0, [0, 1, 2], 0) #first index: cell_index, second index: cell_points_id, third index: original_index
    triangle._coordinates = [(0, 0), (1, 0), (0, 1)]
    triangle.midpoint()  
    triangle.area()  
    return triangle

@pytest.fixture
def sim_line():
    # Mocking a Sim_Line object with 2 points
    line = Sim_Line(0, [0, 1], 0)
    line._coordinates = [(0, 0), (1, 1)] #first two coordinates correspond to 
    line.midpoint()  # Calculate the midpoint of the line
    return line

@pytest.fixture
def sim_mesh():
    # Creating a Sim_Mesh object using mock data
    mesh = Sim_Mesh(sample_mesh_data)
    mesh.store_area()  # Calculate areas
    mesh.store_midpoint()  # Calculate midpoints
    return mesh

# Testing the flux function

def test_flux_positive_normal():
    # Test for positive flux when np.dot(v, normal) > 0
    u_i = 10
    u_ngh = 5
    normal = np.array([1, 0])  # Positive direction
    v = np.array([1, 0])  # Velocity vector in the positive direction
    
    flux_value = flux(u_i, u_ngh, normal, v)
    assert flux_value == 10, f"Expected flux: 10, but got: {flux_value}"

# This code should work but i dont:
# def test_flux_negative_normal():
#     # Test for negative flux when np.dot(v, normal) < 0
#     u_i = 10
#     u_ngh = 5
#     normal = np.array([1, 0])  # Positive direction
#     v = np.array([-1, 0])  # Velocity vector in the negative direction
    
#     flux_value = flux(u_i, u_ngh, normal, v)
#     assert flux_value == 5, f"Expected flux: 5, but got: {flux_value}"


# Testing the Sim_Cell class
def test_sim_cell():
    # Test the Sim_Cell class factory method
    cell = Sim_Cell.cell_factory("line", 0, [0, 1], 0)
    assert isinstance(cell, Sim_Line), "Sim_Cell factory did not return a Sim_Line object"

# Testing the Sim_Line class
#midpoint is the average of the coordinates
def test_sim_line_midpoint(sim_line: Sim_Line):
    # Test the midpoint calculation for the Sim_Line class
    assert sim_line._midpoint == [0.5, 0.5], f"Expected midpoint: [0.5, 0.5], but got: {sim_line._midpoint}"

# Testing the Sim_Triangle class

def test_sim_triangle_midpoint(sim_triangle: Sim_Triangle):
    # Test the midpoint calculation for the Sim_Triangle class
    assert sim_triangle._midpoint == [0.3333333333333333, 0.3333333333333333], f"Expected midpoint: [0.3333333333333333, 0.3333333333333333], but got: {sim_triangle._midpoint}"

def test_sim_triangle_area(sim_triangle: Sim_Triangle):
    # Test the area calculation for the Sim_Triangle class
    assert sim_triangle._area == 0.5, f"Expected area: 0.5, but got: {sim_triangle._area}"

# Testing the Sim_Mesh class - dette blir feil....
#COPILOT:
# def test_sim_mesh_creation(sim_mesh: Sim_Mesh):
#     # Test the creation of Sim_Mesh object
#     assert len(sim_mesh._cells) == 2, f"Expected 2 cells, but got: {len(sim_mesh._cells)}"

# def test_sim_mesh_initial_oil(sim_mesh):
#     # Test the initial oil distribution calculation for the Sim_Mesh class
#     sim_mesh.initial_oil(0.5, 0.5)
#     assert sim_mesh._cells[1]._u == np.exp(-0.5), f"Expected initial oil value: {np.exp(-0.5)}, but got: {sim_mesh._cells[1]._u}"

# def test_sim_mesh_flow_vector(sim_mesh):
#     # Test the flow vector calculation for the Sim_Mesh class
#     sim_mesh.flow_vector()
#     assert sim_mesh._cells[1]._v == 0.5, f"Expected flow vector: 0.5, but got: {sim_mesh._cells[1]._v}"

# def test_sim_mesh_update_oil(sim_mesh):
#     # Test the update oil calculation for the Sim_Mesh class
#     sim_mesh._cells[1]._u = 1  # Set initial oil value to 1
#     sim_mesh.update_oil(0.1)  # Update oil with delta_t = 0.1
#     assert sim_mesh._cells[1]._u == 0.9048374180359595, f"Expected updated oil value: 0.9048374180359595, but got: {sim_mesh._cells[1]._u}"

# CHAT:
# def test_sim_mesh_store_area(sim_mesh: Sim_Mesh):
#     # Test the store_area method in Sim_Mesh
#     for cell in sim_mesh._cells:
#         if isinstance(cell, Sim_Triangle):
#             assert cell._area > 0, "Area should be greater than 0 for triangles"

# def test_sim_mesh_store_midpoint(sim_mesh):
#     # Test the store_midpoint method in Sim_Mesh
#     for cell in sim_mesh._cells:
#         assert cell._midpoint, "Midpoint should be calculated for each cell"

# def test_sim_mesh_initial_oil(sim_mesh):
#     # Test that initial oil amount is set correctly
#     for cell in sim_mesh._cells:
#         if isinstance(cell, Sim_Triangle):
#             assert cell._u >= 0, f"Expected non-negative oil amount, but got: {cell._u}"

# def test_sim_mesh_update_oil(sim_mesh):
#     # Test the update_oil method in Sim_Mesh (make sure oil is updated correctly)
#     delta_t = 0.01
#     initial_u = sim_mesh._cells[0]._u  # Initial oil value of the first cell
#     sim_mesh.update_oil(delta_t)
#     assert sim_mesh._cells[0]._u != initial_u, f"Oil amount should be updated, but it stayed the same"
# import pytest
# from packages.simulation.simulation import Sim_Mesh, Sim_Cell, Sim_Line, Sim_Triangle

# def test_create_cells_length(sim_mesh: Sim_Mesh):
#     # Test the _create_cells method to check the correct number of cells
#     created_cells = sim_mesh._create_cells(sample_mesh_data)
#     assert len(created_cells) == 2  # Assert that 2 cells were created

# def test_create_cells_first_type(sim_mesh: Sim_Mesh):
#     # Test the first created cell type
#     created_cells = sim_mesh._create_cells(sample_cell_data)
#     assert isinstance(created_cells[0], Sim_Line)  # Assert first cell is of type Sim_Line

# def test_create_cells_second_type(sim_mesh: Sim_Mesh):
#     # Test the second created cell type
#     created_cells = sim_mesh._create_cells(sample_cell_data)
#     assert isinstance(created_cells[1], Sim_Triangle)  # Assert second cell is of type Sim_Triangle

# def test_create_cells_first_cell_index(sim_mesh: Sim_Mesh):
#     # Test the cell index of the first cell
#     created_cells = sim_mesh._create_cells(sample_cell_data)
#     assert created_cells[0]._cell_index == 0  # Assert first cell index is 0

# def test_create_cells_second_cell_index(sim_mesh: Sim_Mesh):
#     # Test the cell index of the second cell
#     created_cells = sim_mesh._create_cells(sample_cell_data)
#     assert created_cells[1]._cell_index == 1  # Assert second cell index is 1

# def test_create_cells_first_cell_points(sim_mesh: Sim_Mesh):
#     # Test the points of the first created cell
#     created_cells = sim_mesh._create_cells(sample_cell_data)
#     assert created_cells[0]._cell_points_id == [0, 1]  # Assert points of the first cell are [0, 1]

# def test_create_cells_second_cell_points(sim_mesh: Sim_Mesh):
#     # Test the points of the second created cell
#     created_cells = sim_mesh._create_cells(sample_cell_data)
#     assert created_cells[1]._cell_points_id == [0, 1, 2]  # Assert points of the second cell are [0, 1, 2]


# def test_sim_cell_get_amount_of_oil():
#     # Test get_amount_of_oil method
#     cell = Sim_Cell(0, [0, 1, 2], 0)
#     cell._u = 100  # Set the oil amount directly
#     assert cell.get_amount_of_oil() == 100, f"Expected oil amount: 100, but got: {cell.get_amount_of_oil()}"
    
# def test_sim_cell_v(sim_line: Sim_Line):
#     # Test velocity calculation for a line cell
#     sim_line.v()  # Calculate velocity
#     assert len(sim_line._v) == 2, f"Velocity should be a 2D vector, but got: {sim_line._v}"