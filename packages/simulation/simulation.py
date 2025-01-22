from packages.simulation.msh_classes import Cell, Line, Triangle, Mesh
import numpy as np
import pandas as pd
import os
import ast

def flux(u_i, u_ngh, normal, v):
    """
    A function that calculates the flux value. 
    It checks if the velocity vector is in the same direction as the normal vector, and if so, returns the flux value.
    
    Parameters:
    u_i: amount of oil in cell i at time t_n
    u_ngh : amount of oil in cell ngh at time t_n
    normal: normal of cell i at edge e
    v: velocity field at edge e
    """
    if np.dot(v, normal) > 0:
        return u_i * np.dot(v , normal)
    else:
        return u_ngh * np.dot(v, normal)

class Sim_Cell(Cell):
    """
    A child class that inherits from the Cell class and stores the simulation cells.
    """
    def __init__(self, cell_index, cell_points_id, original_index):
        """
        Initializes the simulation cell with the cell index, cell points id, and original index.

        Parameters:
        cell_index: index of the cell
        cell_points_id: id of the cell points
        original_index: original index

        Stores the midpoint, area, oil amount, velocity, and scaled normals.
        """
        super().__init__(cell_index, cell_points_id, original_index)
        self._midpoint = [] 
        self._area = 0
        self._u = 0
        self._v = []
        self._scaled_normals = []
        self._inside_area = False
    
    def v(self):
        """
        A function that calculates the velocity field for the simulation cells.
        
        Variables:
        x: x-coordinate of the midpoint in the cell
        y: y-coordinate of the midpoint in the cell
        """
        x, y = self._midpoint 
        self._v = np.array([y-0.2*x, -x])

    def get_amount_of_oil(self):
        """
        A getter function that returns the amount of oil in the cell.
        """
        return self._u

    @staticmethod
    def cell_factory(cell_type, cell_index, cell_points_id, original_index):
        """
        Factory method to create simulation cells based on the cell type.
        Overrides the base class's cell_factory to create simulation cells

        Parameters:
        cell_type: type of the cell
        cell_index: index of the cell
        cell_points_id: id of the cell points
        original_index: id of the cell 
        """
        if cell_type.lower() == "triangle":
            return Sim_Triangle(cell_index, cell_points_id, original_index)  # Sim_Triangle is a simulation-specific class
        elif cell_type.lower() == "line":
            return Sim_Line(cell_index, cell_points_id, original_index)  # Sim_Line is a simulation-specific class
        else:
            raise ValueError(f"Unknown cell type: {cell_type}")

class Sim_Line(Sim_Cell, Line):
    """
    Class for simulation line cells. Inherits from its parents class; Line and Sim_Cell.
    """
    def midpoint(self):
        """
        A function that calculates the midpoint of the line.
        
        Variables:
        x1, y1: x- and y-coordinate of the first point in the line[0]
        x2, y2: x- and y-coordinate of the second point in the line[1]
        """
        x1,y1 = self._coordinates[0]
        x2,y2 = self._coordinates[1]
        self._midpoint = [(x1 + x2) / 2, (y1 + y2) / 2]

class Sim_Triangle(Sim_Cell, Triangle):
    """
    Class for simulation triangle cells. Inherits from its parents classes; Sim_Cell and Triangle from the msh_classes file.
    It stores the midpoint, area, oil amount, velocity, and scaled normals.
    """
    def scaled_normals(self):
        """
        A function that calculates the scaled normals for the simulation triangle cells.
        
        Variables:
        pointer1: list of pointers to the first, second, and third points in the triangle
        pointer2: list of pointers to the second, third, and first points in the triangle
        midpoint: midpoint of the triangle

        For each pair of pointers, calculate the normal vector, orthonormal vector, and scaled normal vector.
        Check if the scaled normal vector is pointing in the correct direction and store it with the neighbor cell.
        """
        pointer1 = [0,1,2]
        pointer2 = [1,2,0]
        midpoint = self._midpoint

        for i,j in zip(pointer1, pointer2):
            p_j = self._coordinates[j]
            p_i = self._coordinates[i]
            e_vector = np.subtract(p_j, p_i)
            normal = [e_vector[1], -e_vector[0]]  # [e[1], -e[0]] = [dy, -dx]
            orthonormal = normal / np.linalg.norm(normal)

            check_vector = np.subtract(p_i, midpoint)
            scaled_normals = orthonormal * np.linalg.norm(e_vector)
            if np.dot(orthonormal, check_vector) < 0:
                scaled_normals = np.flip(scaled_normals)
            
            for ngh in self._neighbors:
                for neighbor_cell, shared_points in ngh.items():
                    if np.isin(self._cell_points_id[i], shared_points) and np.isin(self._cell_points_id[j], shared_points):
                        # Store the scaled normal vector with the neighbor cell as the key
                        self._scaled_normals.append({neighbor_cell: scaled_normals})


    def __str__(self):  # prints info
        return f"Triangle {self._original_index}, Oil: {self.get_amount_of_oil()}\
             Normals:{self._scaled_normals} Neighbors:{self._neighbors} Velocity:{self.get_flowfield()}"
    
    def area(self):
        """
        A function that calculates the area of the triangle.
        
        Variables:
        x1, y1: x- and y-coordinates of the first point in the triangle
        x2, y2: x- and y-coordinates of the second point in the triangle
        x3, y3: x- and y-coordinates of the third point in the triangle
        """
        x1, y1 = self._coordinates[0]
        x2, y2 = self._coordinates[1]
        x3, y3 = self._coordinates[2]

        self._area = 0.5 * np.abs((x1 - x3) * (y2 - y1) - (x1 - x2) * (y3 - y1))

    def midpoint(self):
        """
        A function that calculates the midpoint of the triangle.
        
        Variables:
        x1, y1: x- and y-coordinates of the first point in the triangle
        x2, y2: x- and y-coordinates of the second point in the triangle
        x3, y3: x- and y-coordinates of the third point in the triangle
        """
        x1, y1 = self._coordinates[0]
        x2, y2 = self._coordinates[1]
        x3, y3 = self._coordinates[2]

        self._midpoint = [(x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3]
    
    def u_0(self, x, y):
        """
        A function that calculates the initial oil amount for the simulation triangle cells.
        
        Parameters:
        x, y: x- and y-coordinate of the triangle cells

        Variables:
        x1, y1: x- and y-coordinates of the midpoint in the triangle
        vector: vector between the midpoint and the x- and y-coordinates
        norm: normal of the vector
        """
        x1, y1 = self._midpoint
        vector = np.array([x1-x, y1-y])
        norm = np.linalg.norm(vector)
        
        self._u = np.exp(-(norm**2/0.01))

    def up(self, delta_t, mesh_cells):
        """
        A function that calculates the updated oil amount for the simulation triangle cells.
        This updated value is added to the initial oil amount.
        
        Parameters:
        delta_t: time step
        mesh_cells: list of all cells in the mesh
        
        Variables:
        up: updated oil amount, initialized to 0
        ngh_data: data of the scaled normals of the neighbors
        ngh_cell_id: id of the neighbor cell
        scaled_normal: scaled normal of the neighbor cell
        v: velocity field
        flux_value: flux value between the current cell and the neighbor cell
        """
        up = 0

        for ngh_data in self._scaled_normals:
            for ngh_cell_id, scaled_normal in ngh_data.items():
                ngh_cell_id = int(ngh_cell_id)

                v = 0.5 * (self._v + mesh_cells[ngh_cell_id]._v)  
                flux_value = flux(self._u, mesh_cells[ngh_cell_id]._u, scaled_normal, v)
                up -= delta_t / self._area * flux_value
            
        self._u = self._u + up



class Sim_Mesh(Mesh):
    #make a list of cell ids that are inside the area to append to
    """
    Class for simulation mesh. Inherits from its parents class; Mesh from the msh_classes file.
    """

    def __init__(self, msh):
        """
        Initializes the simulation mesh with the mesh data. 
        Stores the points inside the area.
        """
        super().__init__(msh)
        self._points_inside_area = []

    def _create_cells(self, mesh_cells):
        """
        A function that creates the cells in the mesh.
        The function loops through the mesh-cells and creates the cells using the cell_factory function
        and stores them in the Cell class.
        
        Parameters:
        mesh_cells: list of cells in the mesh
        
        Variables:
        all_cells: list of all cells in the mesh
        orginal_cell_id: original index of the cell
        """
        all_cells = []
        orginal_cell_id = 0
        for cell_block in mesh_cells: 
            cell_type = cell_block.type  # Access the type of the cell (e.g., "triangle", "line")
            if cell_type == "vertex":
                continue

            cell_data = cell_block.data  # Access the array of cell points
            """uses metadata to utilize cell factory for each cell type"""
            for idx, cell_points_id in enumerate(cell_data): # idx is id for cell in blocktype
                all_cells.append(Sim_Cell.cell_factory(cell_type, idx, cell_points_id, orginal_cell_id))
                orginal_cell_id += 1
        return all_cells

    def store_area(self):
        """
        A function that stores the area for all triangle cells in the mesh using the .area() function.
        """
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):
                cell.area()
        print("Area calculated for all triangle cells in mesh")
    
    def store_midpoint(self):
        """
        A function that stores the midpoint for all cells in the mesh using the .midpoint() function.
        """
        for cell in self._cells:
            cell.midpoint()
        print("Midpoint calculated for all cells in mesh")
        
    def initial_oil(self, x, y):
        """
        A function that calculates the initial oil amount for all triangle cells in the mesh using the .u_0() function.
        """
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):    
                cell.u_0(x, y)
        print("Initial oil calculated for all triangle cells in mesh")
    
    def flow_vector(self):
        """
        A function that calculates the flow field for all cells in the mesh using the .v() function.
        """
        for cell in self._cells:          
            cell.v()
        print("Flowfiels calculated for all cells in mesh")

    def update_oil(self, delta_t):
        """
        A function that updates the oil amount for all triangle cells in the mesh using the .up() function.
        """
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):
                cell.up(delta_t, self._cells)
    
    def normal(self):
        """
        A function that calculates the scaled normals for all triangle cells in the mesh using the .scaled_normals() function.
        """
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):
                cell.scaled_normals()
        print("Normals calculated for all cells in mesh")

    def cells_inside_area(self, area:list):
        """
        A function that finds the cells inside the area and appends them to the _points_inside_area list.
        """
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):
                x, y = cell._midpoint
                
                x_val = area[0]
                y_val = area[1]

                if min(x_val) <= x <= max(x_val)\
                and min(y_val) <= y <= max(y_val):
                    self._points_inside_area.append(cell._original_index)
        
        print("Cells inside area found")
                    
    def store_mesh_sim(self, destination_folder = None, filename = "restartfile.csv"):
        """
        A function that stores the mesh data in a csv file to make it easier to restart the simulation at a chosen time.
        """
        mesh_data = []
        for cell in self._cells:
            cell_data = {
                'cell_index': cell._cell_index,
                'orginal_cell_index': cell._original_index,
                'cell_type': type(cell).__name__,
                'coordinates': str(cell._coordinates),
                'neighbors': str(cell._neighbors) if cell._neighbors else None,
                'velocity': str(cell._v),
                'midpoint': str(cell._midpoint) if isinstance(cell, Sim_Cell) else None,
                'area': cell._area if isinstance(cell, Sim_Cell) else None,
                'oil_amount': cell.get_amount_of_oil() if isinstance(cell, Sim_Cell) else None,
                'scaled_normals': str(cell._scaled_normals) if isinstance(cell, Sim_Cell) else None
            }
            mesh_data.append(cell_data)

        df = pd.DataFrame(mesh_data)
        
        if filepath:
            filepath = os.path.join(destination_folder, filename)
        else:
            filepath = filename

        df.to_csv(filepath, index = False)

        print(f"Data stored and written to file {filepath}.csv")

def reconstruct_mesh(filename = "restartfile.csv"):
        
    df = pd.read_csv(filename)

    reconstructed_cells = []

    for index, row in df.iterrows():
        cell_type = row['cell_type']
        coordinates = ast.literal_eval(row['coordinates'])  # Convert string back to list of tuples
        neighbors = ast.literal_eval(row['neighbors']) if row['neighbors'] != "None" else None
        velocity = np.array(ast.literal_eval(row['velocity']))  # Convert string to numpy array
        midpoint = ast.literal_eval(row['midpoint']) if pd.notna(row['midpoint']) else None
        area = row['area']
        oil_amount = row['oil_amount']
        scaled_normals = ast.literal_eval(row['scaled_normals']) if pd.notna(row['scaled_normals']) else None

        # Create the correct type of cell (e.g., Sim_Triangle or Sim_Line)
        if cell_type == "Sim_Triangle":
            cell = Sim_Triangle(coordinates, velocity, neighbors, midpoint, area, oil_amount, scaled_normals)
        elif cell_type == "Sim_Line":
            cell = Sim_Line(coordinates, velocity, neighbors, midpoint, area, oil_amount, scaled_normals)
        # Add more cell types as necessary

        # Set the attributes based on the row data
        cell._cell_index = row['cell_index']
        cell._original_index = row['original_index']

        # Append the reconstructed cell to the list
        reconstructed_cells.append(cell)

    # Assuming mesh object has a _cells attribute that holds the list of cells
    self._cells = reconstructed_cells

    print(f"Mesh successfully reconstructed from {filename}")

    reconstructed_mesh = Sim_Mesh(msh=None)  
    reconstructed_mesh._cells = reconstructed_cells 
    return reconstructed_mesh

