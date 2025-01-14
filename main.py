from msh_classes import *
import meshio as m
import numpy as np
import matplotlib.pyplot as plt
import os

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

    umax = max(cell.get_amount_of_oil() for cell in mesh._cells if isinstance(cell, Triangle))
    umin = min(cell.get_amount_of_oil() for cell in mesh._cells if isinstance(cell, Triangle))

# Iterate through time steps and plot the mesh
for timestep in range(20):
    # Update oil distribution
    mesh.update_oil(delta_t=0.001)

    # Create the plot
    plt.figure()
    ax = plt.gca()

    # Create the colormap
    sm = plt.cm.ScalarMappable(cmap="viridis")
    sm.set_array([umin, umax])
    cbar = plt.colorbar(sm, ax=ax, label="Oil Concentration (u)")

    # Plot each triangle with its corresponding color
    for cell in mesh._cells:
        if isinstance(cell, Triangle):
            # Get triangle vertices
            vertices = np.array(cell._coordinates)

            # Get oil concentration `u` for the cell
            u_value = cell.get_amount_of_oil()

            # Normalize u_value for colormap
            normalized_u = (u_value - umin) / (umax - umin)

            # Add the triangle to the plot
            ax.add_patch(
                plt.Polygon(vertices, color=plt.cm.viridis(normalized_u), edgecolor="black", alpha=0.9)
            )

    # Add labels to axes
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    ax.set_aspect("equal", adjustable="box")

    # Save the plot
    image_path = os.path.join("./images", f"mesh_timestep_{timestep}.png")
    plt.savefig(image_path)

    # Close the plot to avoid memory issues
    plt.close()