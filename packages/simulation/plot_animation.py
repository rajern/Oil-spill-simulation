import os
import matplotlib.pyplot as plt
import cv2  # requires opencv-python


def plot(mesh, destination_folder: str, nr_of_pics: int, timesteps: int):
    
    N = timesteps/nr_of_pics

    umax = max(cell.get_amount_of_oil() for cell in mesh._cells if isinstance(cell, Sim_Triangle))
    umin = min(cell.get_amount_of_oil() for cell in mesh._cells if isinstance(cell, Sim_Triangle))

    # Iterate through time steps and plot the mesh
    for pic in range(nr_of_pics):
        plt.figure()
        ax = plt.gca()

        # Create the colormap
        sm = plt.cm.ScalarMappable(cmap="viridis")
        sm.set_array([umin, umax])
        cbar = plt.colorbar(sm, ax=ax, label="Oil Concentration (u)")

        # Plot each triangle with its corresponding color
        for cell in mesh._cells:
            if isinstance(cell, Sim_Triangle):
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
        image_path = os.path.join("./" + destination_folder, f"mesh_timestep_{pic}.png")
        plt.savefig(image_path)

        # Close the plot to avoid memory issues
        plt.close()
        
        # Update oil distribution
        for timestep in range(N):
            mesh.update_oil(delta_t=0.001)
            print(mesh._cells[500]._u)

        # Create the plot


def animation(folder: str, img_name: str, nr_of_pics: int):
    # Get the list of image files in the directory
    images = [f"{folder}/{img_name}{i}.png" for i in range(0, nr_of_pics)]
    # determine dimension from first image
    frame = cv2.imread(images[0])
    height, width, layers = frame.shape
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # or 'XVID', 'DIVX', 'mp4v' etc.
    video = cv2.VideoWriter("video.AVI", fourcc, 5, (width, height))  # 5 frames per second
    for image in images:
        video.write(cv2.imread(image))
        cv2.destroyAllWindows()
        video.release()
