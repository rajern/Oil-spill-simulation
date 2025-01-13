from msh_classes import *
import meshio as m
import numpy as np

if __name__ == "__main__":
    msh_name = "./input_data/bay.msh"
    msh = m.read(msh_name)
    mesh = Mesh(msh)
    x=0.35
    y=0.45
    mesh.store_coordinates()
    mesh.store_midpoint()
    mesh.find_neighbors_and_normals()
    mesh.flow_vector()
    mesh.initial_oil(x, y)
    mesh.store_area()
    mesh.update_oil(0.1)

    print(f"{mesh._cells[189]}")



# i = point_in_triangle(0.35, 0.45)


