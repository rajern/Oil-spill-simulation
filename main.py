from msh_classes import *
import meshio as m
import numpy as np

"""
msh_name = "./input_data/bay.msh"
msh = m.read(msh_name)

mesh_instance = mesh(msh)
mesh_instance.find_neighbors()
"""
if __name__ == "__main__":
    msh_name = "./input_data/bay.msh"
    msh = m.read(msh_name)

    mesh_instance = mesh(msh)
    mesh_instance.find_neighbors()

