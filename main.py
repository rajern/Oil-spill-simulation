from msh_classes import *
from packages.simulation.simulation import *
import meshio as m
import numpy as np
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    msh_name = "./input_data/bay.msh"
    msh = m.read(msh_name)
    mesh = Sim_Mesh(msh)
   #x, y = 0.35, 0.45
    mesh.store_coordinates()
    mesh.store_midpoint()
    mesh.normal()
    mesh.find_neighbors()
    #mesh.find_neighbors_and_normals()
    #mesh.flow_vector()
    #mesh.initial_oil(x, y)
    #mesh.store_area()

   