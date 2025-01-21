from packages.simulation.msh_classes import *
from packages.simulation.simulation import *
from packages.simulation.plot_animation import *
import meshio as m
import numpy as np
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    msh_name = "./input_data/bay.msh"
    msh = m.read(msh_name)
    mesh = Sim_Mesh(msh)

    mesh.store_coordinates()
    mesh.store_midpoint()
    mesh.find_neighbors()
    mesh.normal()
    mesh.flow_vector()
    x, y = 0.35, 0.45
    mesh.initial_oil(x, y)
    mesh.store_area()
    area = [[0.0,0.45], [0.0,0.2]]
    mesh.cells_inside_area(area)
    plot(mesh, "images", 20, 1000, delta_t, area)

    animation("images", "mesh_timestep_", 20)

    mesh.store_mesh_sim()
   