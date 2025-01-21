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


# Testing the flux function

def test_flux_positive_normal():
    # Test for positive flux when np.dot(v, normal) > 0
    u_i = 10
    u_ngh = 5
    normal = np.array([1, 0])  # Positive direction
    v = np.array([1, 0])  # Velocity vector in the positive direction
    
    flux_value = flux(u_i, u_ngh, normal, v)
    assert flux_value == 10, f"Expected flux: 10, but got: {flux_value}"

# Testing flux function the other way around
def test_flux_negative_normal():
    # Test for negative flux when np.dot(v, normal) < 0
    u_i = 10
    u_ngh = 5
    normal = np.array([1, 0])  # Positive direction
    v = np.array([-1, 0])  # Velocity vector in the negative direction
    
    flux_value = flux(u_i, u_ngh, normal, v)
    assert flux_value == -5, f"Expected flux: 5, but got: {flux_value}"


# Testing the Sim_Cell class
def test_sim_cell():
    # Test the Sim_Cell class factory method
    cell = Sim_Cell.cell_factory("line", 0, [0, 1], 0)
    assert isinstance(cell, Sim_Line), "Sim_Cell factory did not return a Sim_Line object"

# Testing the Sim_Line class
# midpoint is the average of the coordinates
def test_sim_line_midpoint(sim_line: Sim_Line):
    # Test the midpoint calculation for the Sim_Line class
    assert sim_line._midpoint == [0.5, 0.5], f"Expected midpoint: [0.5, 0.5], but got: {sim_line._midpoint}"

# Additional test cases for Sim_Mesh and related classes

# Testing Sim_Triangle calculations
def test_sim_triangle_area():
    triangle = sim_triangle()
    expected_area = 0.5
    assert triangle._area == expected_area, f"Expected area: {expected_area}, but got: {triangle._area}"

def test_sim_triangle_midpoint():
    triangle = sim_triangle()
    expected_midpoint = [1/3, 1/3]
    assert np.allclose(triangle._midpoint, expected_midpoint), f"Expected midpoint: {expected_midpoint}, but got: {triangle._midpoint}"

def test_sim_triangle_initial_oil():
    triangle = sim_triangle()
    x, y = 0.1, 0.1  # Point near the triangle's midpoint
    triangle.u_0(x, y)
    expected_u = np.exp(-((1/3 - x)**2 + (1/3 - y)**2) / 0.01)
    assert np.isclose(triangle._u, expected_u), f"Expected oil amount: {expected_u}, but got: {triangle._u}"

# Testing Sim_Line calculations
def test_sim_line_velocity(sim_line: Sim_Line):
    sim_line.v()
    expected_velocity = [0.5 - 0.2 * 0.5, -0.5]  # [y-0.2*x, -x] at midpoint (0.5, 0.5)
    assert np.allclose(sim_line._v, expected_velocity), f"Expected velocity: {expected_velocity}, but got: {sim_line._v}"
