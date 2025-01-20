from msh_classes import *
import meshio as m
import numpy as np
import matplotlib.pyplot as plt
import os
from readToml import ConfigReader
import argparse

def parse_input():
    parser = argparse.ArgumentParser(description = 'Simulation configuration')

    # Add command-line arguments
    parser.add_argument(
        '--find_all', action='store_true', help = 'Find all config files in the main program folder'
    )
    parser.add_argument(
        '-f', '--folder', help = 'Specify folder to search for config files', type=str   
    )
    parser.add_argument(
        '-c', '--config_file', help = 'Specify a single config file to read', type=str
    )
    args = parser.parse_args()

    find_all = args.find_all
    folder = args.folder
    config_file = args.config_file

    return find_all, folder, config_file

if __name__ == "__main__":
    find_all, folder, config_file = parse_input()

    if config_file:
        # Process a specific config file
        config_files = [config_file]

    elif find_all:
        # Find all .toml files in a folder 
        search_folder = os.getcwd() # Get current working directory - getcwd()
        config_files = []

        for file in os.listdir(search_folder): # Creates list of all entries in the directory
            if file.endswith('.toml'): 
                config_files.append(os.path.join(search_folder, file)) # Os.path.join() ensures file gets a proper path

            if not config_files: 
                raise ValueError(f'No config files found in folder {search_folder}')

    elif folder:
        # Search for .toml files in the specified folder
        search_folder = folder
        config_files = []

        for file in os.listdir(search_folder):
            if file.endswith('.toml'): 
                config_files.append(os.path.join(search_folder, file)) # Os.path.join() ensures file gets a proper path

            if not config_files: 
                raise ValueError(f'No config files found in folder {search_folder}')

    else:
        # Using 'input.toml' if no arguments are provided
        config_files = ["input.toml"]

    for config_file in config_files: 
        try: 
            # Load configuration file
            config_reader = ConfigReader(config_file)
            config_reader.load_config_file()
            
            # Extract folder name from config file
            results_folder = config_file.replace('.toml', '')

            # Create folder if it doesn't already exist
            if not os.path.exists(results_folder):
                os.makedirs(results_folder)
            
            # Access values from the configuration
            n_steps = config_reader.get_value("settings", "nSteps")
            t_start = config_reader.get_value("settings", "tStart")
            t_end = config_reader.get_value("settings", "tEnd")
            delta_t = (t_end - t_start) / n_steps # Add delta_t for later
            mesh_name = config_reader.get_value("geometry", "meshName")
            borders = config_reader.get_value("geometry", "borders") # Fishing grounds
            log_name = config_reader.get_value("IO", "logName")
            write_frequency = config_reader.get_value("IO", "writeFrequency") # Use this value for creating video
            restart_file = config_reader.get_value("IO", "restartFile")

            # Debugging: Print configuration values
            print(f"Loaded configuration:")
            print(f"nSteps: {n_steps}, tStart: {t_start}, tEnd: {t_end}")
            print(f"Mesh Name: {mesh_name}, Borders: {borders}")
            print(f"Log Name: {log_name}, Write Frequency: {write_frequency}")
            if restart_file:
                print(f"Restart File: {restart_file}")

            # Proceed with the main logic
            msh_name = mesh_name
            msh = m.read(msh_name)
            mesh = Mesh(msh)
            x, y = 0.35, 0.45
            mesh.store_coordinates()
            mesh.store_midpoint()
            mesh.find_neighbors_and_normals()
            mesh.flow_vector()
            mesh.initial_oil(x, y)
            mesh.store_area()

            umax = max(cell.get_amount_of_oil() for cell in mesh._cells if isinstance(cell, Triangle))
            umin = min(cell.get_amount_of_oil() for cell in mesh._cells if isinstance(cell, Triangle))

            # Iterate through time steps and plot the mesh
            for timestep in range(n_steps): # n-steps input
                # Update oil distribution
                mesh.update_oil(delta_t) 
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
                        vertices = np.array(cell._coordinates)
                        u_value = cell.get_amount_of_oil()
                        normalized_u = (u_value - umin) / (umax - umin)
                        ax.add_patch(
                            plt.Polygon(vertices, color=plt.cm.viridis(normalized_u), edgecolor="black", alpha=0.9)
                        )

                # Add labels to axes
                plt.xlabel("X-coordinate")
                plt.ylabel("Y-coordinate")
                ax.set_aspect("equal", adjustable="box")

                # Save the plot
                image_path = os.path.join(results_folder, f"mesh_timestep_{timestep}.png")
                plt.savefig(image_path)

                # Close the plot 
                plt.close()

        except Exception as e:
            print(f"Error: {e}")
            exit(1)
