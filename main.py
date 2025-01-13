from msh_classes import *
import meshio as m
import numpy as np

if __name__ == "__main__":
    msh_name = "./input_data/bay.msh"
    msh = m.read(msh_name)

    mesh = Mesh(msh)
    mesh.store_coordinates()
    mesh.store_midpoint()
    mesh.find_neighbors_and_normals()
    mesh.flow_vector()
    mesh.initial_oil()
    mesh.store_area()

    print(f"{mesh._cells[189]}")



# i = point_in_triangle(0.35, 0.45)
# ngh = i._neighbors
# A_i = i.area()
# V_i_l = #scaled normal of cell i ad edge e 
# V_i_l = i/np.linalg.norm(i) #normalized normal of cell i at edge e???????
# v_i = #velocity field at midpoint of cell i
# v_ngh = #velocity field at midpoint of cell ngh
# u_i = #amount of oil in cell i at time t_n
# u_ngh = #amount of oil in cell ngh at time t_n
# delta_t = t_n - t_i #time step?????

# v = 0.5 * (v_i + v_ngh) #average velocity field at edge e

# #flux from cell i to cell ngh
# F_i_ngh = (-delta_t / A_i) * g * (u_i , u_ngh , V_i_l, v)
#   if np.dot(v, V_i_l) > 0:
#       g(a, b, V_i_l, v) = a * np.dot(v, V_i_l)
#   else:
#       g(a, b, V_i_l, v) = b * np.dot(v, V_i_l)

