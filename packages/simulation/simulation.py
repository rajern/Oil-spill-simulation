from .msh_classes import Cell, Line, Triangle, Mesh
import numpy as np
"""
Class used for the simulation of the cells. 
It inherits from its parents class; Cell from the msh_classes file.
"""

def flux(u_i, u_ngh, normal, v):
    """
    Calculates the flux value between two cells. Variables:
        u_i: amount of oil in cell i at time t_n
        u_ngh: amount of oil in cell ngh at time t_n
        norm: normal of cell i at edge e
        v: velocity field at edge e
    """
    if np.dot(v, normal) > 0:
        return u_i * np.dot(v , normal)
    else:
        return u_ngh * np.dot(v, normal)

class Sim_Cell(Cell):
    """
    Class for simulation cells. Inherits from its parents class; Cell from the msh_classes file.
    It stores the midpoint, area, oil amount, velocity, and scaled normals.
    """
    def __init__(self, cell_index, cell_points_id, original_index):
        super().__init__(cell_index, cell_points_id, original_index)

        self._midpoint = [] 
        self._area = 0
        self._u = 0
        self._v = []
        self._scaled_normals = []
    
    def v(self):
        x, y = self._midpoint 
        
        self._v = np.array([y-0.2*x, -x])

    def get_amount_of_oil(self):
        return self._u


    @staticmethod
    def cell_factory(cell_type, cell_index, cell_points_id, original_index):
        '''Overrides the base class's cell_factory to create simulation cells'''
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
        x1,y1 = self._coordinates[0]
        x2,y2 = self._coordinates[1]

        self._midpoint = [(x1 + x2) / 2, (y1 + y2) / 2]

class Sim_Triangle(Sim_Cell, Triangle):
    
    def scaled_normals(self):
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
                        print({neighbor_cell: scaled_normals})  # print the scaled normal vector for debugging


    def __str__(self):  # prints info
        return f"Triangle {self._original_index}, Oil: {self.get_amount_of_oil()}\
             Normals:{self._scaled_normals} Neighbors:{self._neighbors} Velocity:{self.get_flowfield()}"
    
    def area(self):
        x1, y1 = self._coordinates[0]
        x2, y2 = self._coordinates[1]
        x3, y3 = self._coordinates[2]

        self._area = 0.5 * np.abs((x1 - x3) * (y2 - y1) - (x1 - x2) * (y3 - y1))

    def midpoint(self):
        x1, y1 = self._coordinates[0]
        x2, y2 = self._coordinates[1]
        x3, y3 = self._coordinates[2]

        self._midpoint = [(x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3]
    
    def u_0(self, x, y):
        x1, y1 = self._midpoint
        vector = np.array([x1-x, y1-y])
        norm = np.linalg.norm(vector)
        
        self._u = np.exp(-(norm**2/0.01))

    def up(self, delta_t, mesh_cells):
        up = 0

        for ngh_data in self._scaled_normals:
            for ngh_cell_id, scaled_normal in ngh_data.items():
                ngh_cell_id = int(ngh_cell_id)

                v = 0.5 * (self._v + mesh_cells[ngh_cell_id]._v)  
                flux_value = flux(self._u, mesh_cells[ngh_cell_id]._u, scaled_normal, v)
                up -= delta_t / self._area * flux_value
            
        self._u = self._u + up


class Sim_Mesh(Mesh):
    
    def _create_cells(self, mesh_cells):
        """Reads cells metadata and stores in list"""
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
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):
                
                cell.area()
    
    def store_midpoint(self):
        for cell in self._cells:
            
            cell.midpoint()
        
    def initial_oil(self, x, y):
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):
                
                cell.u_0(x, y)
    
    def flow_vector(self):
        for cell in self._cells:
                          
            cell.v()
    
    def update_oil(self, delta_t):
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):
                
                cell.up(delta_t, self._cells)
    
    def normal(self):
        for cell in self._cells:
            if isinstance(cell, Sim_Triangle):
                
                cell.scaled_normals()

    def store_mesh_sim(self, filename = "restartfile.txt"):
        with open(filename, "w") as f:
            f.write("Mesh info:\n==========\n")

            for cell in self._cells:
                f.write(f"\nCell index: {cell._cell_index}\n")
                f.write(f"Orginal cell index: {cell._original_index}\n")
                f.write(f"Cell type: {type(cell).__name__}\n")

                f.write("Coordinates: ")
                f.write(", ".join([f"({coord[0]}, {coord[1]})" for coord in cell._coordinates]))
                f.write("\n")
            
                if cell._neighbors:
                    f.write(f"Neighbors: {', '.join(map(str, cell._neighbors))}\n")
                else:
                    f.write("Neighbors: None\n")

                f.write(f"Velocity (v): {cell._v}\n")

                if isinstance(cell, Sim_Cell):
                    f.write(f"Midpoint: {cell._midpoint}\n")
                    f.write(f"Area: {cell._area}\n")
                    f.write(f"Oil Amount (u): {cell.get_amount_of_oil()}\n")
                    f.write(f"Scaled Normals: {cell._scaled_normals}\n")

                f.write("-" * 40 + "\n")

        print(f"Data written to file {filename}")
                
