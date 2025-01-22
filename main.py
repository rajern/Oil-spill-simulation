import os
import meshio as m
import numpy as np
import matplotlib.pyplot as plt
import logging
from packages.simulation.msh_classes import *
from packages.simulation.simulation import *
from packages.simulation.plot_animation import *
from packages.simulation.readToml import *
from packages.simulation.logger import *

if __name__ == "__main__":
    """
    Main function to run the simulation.
    """
    # Parse input arguments
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

    # Process each config file
    for config_file in config_files: 
        try: 
            # Load configuration file
            config_reader = ConfigReader(config_file)
            config_reader.load_config_file()
            
            # Extract folder name and create folder if it doesn't exist
            results_folder = config_file.replace('.toml', '')
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
            
            make_logger(log_name,results_folder)
            log_sim_parameters(n_steps, t_start, t_end, mesh_name, borders, write_frequency, restart_file)


            # Initialize mesh and set up simulation
            msh = m.read(mesh_name)
            mesh = Sim_Mesh(msh)

            mesh.store_coordinates()
            mesh.store_midpoint()
            mesh.find_neighbors()
            mesh.normal()
            mesh.flow_vector()
            x, y = 0.35, 0.45
            mesh.initial_oil(x, y)
            mesh.store_area()
            fishing_bay = borders
            mesh.cells_inside_area(fishing_bay)

            # Run simulation and generate outputs
            plot(mesh, results_folder, write_frequency, n_steps, delta_t, fishing_bay)
            animation(results_folder, "mesh_timestep_", write_frequency)
            mesh.store_mesh_sim(results_folder)

        except Exception as e:
            print(f"Error processing {config_file}: {e}")
            exit(1)