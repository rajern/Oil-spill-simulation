import meshio
from abc import ABC, abstractmethod
import numpy as np
#kake

class Point:
    '''class for point of x and y cord.
    input: all the points in the mesh, cell points index'''
    def __init__(self, points, point_index):
        self._point_index = point_index
        self._x, self._y = points[point_index][:2] #2D mesh

    def __repr__(self): #Returning point desc.
        return f"Point(index={self._point_index}, x={self._x:.2f}, y={self._y:.2f})"
    

class Cell(ABC):
    '''class for cells
    input: cells id, cell points id, the orginal cell id'''
    def __init__(self, cell_index, cell_points_id, original_index):
        self._cell_index = cell_index
        self._original_index = original_index  
        self._cell_points_id = cell_points_id
        self._neighbors = [] #empty list for neigbor cells to be stored
        self._is_boundary = False #boundary statement is false by default

        self._coordinates = []
        
        self._midpoint = [] 
        self._area = 0
        self._u = 0
        self._v = []
        self._scaled_normals = []

    #@abstractmethod #Requires all child classes of Cell to have this func, or it's not valid
    def store_neighbors(self, all_cells):
        pass

    @staticmethod #cell factory for all types of cells 
    def cell_factory(cell_type, cell_index, cell_points_id, original_index):
        if cell_type.lower() == "triangle":
            return Triangle(cell_index, cell_points_id, original_index)
        elif cell_type.lower() == "line":
            return Line(cell_index, cell_points_id, original_index)
        else:
            raise ValueError(f"Unknown cell type: {cell_type}")
        
    def point_coord(self, point_id, mesh_points): #Method for converting points to x-, y- coordinates
        point_obj = mesh_points[point_id]
        return point_obj._x, point_obj._y
    
    def get_point_coord(self, mesh_points):
        self._coordinates = [self.point_coord(point_id, mesh_points) for point_id in self._cell_points_id]
        

class Line(Cell): #line class, parent class: cell
    #finds neighbors and stores in list
    def store_neighbors(self, all_cells):
        for other_cell in all_cells: #checks all cells in mesh
            if self._cell_index != other_cell._cell_index: #ensures diff. cells
                shared_points = set(self._cell_points_id) & set(other_cell._cell_points_id) #hashes for pair points of cells
                if isinstance(other_cell, Line) and len(shared_points) == 1: #if more or equal to 1 shared point, the other cell is a neighbor
                    self._neighbors.append(other_cell._cell_index) #adds to list
                    self._is_boundary = True
                    
                elif len(shared_points) == 2:
                    self._neighbors.append(other_cell._cell_index) #adds to list

    def __str__(self): #prints info
        return f"Line {self._original_index}, Boundary: {self._is_boundary}, Neighbors: {self._neighbors}"

class Triangle(Cell): #triangle class, parent class: cell
    #finds neighbors and corresponding scaled normal vectors, and stores in list
    def store_neighbors_scaled_normal(self, all_cells, mesh_points):
        for other_cell in all_cells: #checks all cells in mesh
            if self._cell_index != other_cell._cell_index: #checks diff. cell
                shared_points = set(self._cell_points_id) & set(other_cell._cell_points_id) #hashes for pair points of cells
                if len(shared_points) == 2: #if equal to 2 shared points, the othe cell is a neighbor
                    self._neighbors.append(other_cell._cell_index) #adds to list
                    
                    shared_points_list = list(shared_points) #converts to list
                    p1 = shared_points_list[0] #defines points
                    p2 = shared_points_list[1]

                    x1,y1 = self.point_coord(p1, mesh_points) #gets x-, y- coordinates for points
                    x2,y2 = self.point_coord(p2, mesh_points)
                    
                    p1=[x1,y1] #defines vectors
                    p2=[x2,y2]

                    dx = x2 - x1 
                    dy = y2 - y1

                    normal = [-dy,dx] #defines normal

                    e_vector = [p2[0] - p1[0], p2[1] - p1[1]] #defines vector for side

                    check_vector = [p1[0] - self._midpoint[0], p1[1] - self._midpoint[1]] #p-vector - x_mid-vector

                    dot_product = check_vector[0] * normal[0] + check_vector[1] * normal[1]
                    
                    if dot_product > 0:
                        o_normal = normal / np.linalg.norm(normal)
                        self._scaled_normals.append(o_normal * np.linalg.norm(e_vector))

                    else:
                        o_normal = normal / np.linalg.norm([dy,-dx])
                        self._scaled_normals.append(o_normal * np.linalg.norm(e_vector))

                    #boundary check
                    if isinstance(other_cell, Line): #checks if neighbor cell is a line
                        self._is_boundary = True
    
    def __str__(self): #prints info
        return f"Triangle {self._original_index}, Midpoint: {self._midpoint} Normals:{self._scaled_normals}"
    
    def point_in_cell(self, x, y, mesh_points):
        x1,y1 = self._coordinates[0]
        x2,y2 = self._coordinates[1]
        x3,y3 = self._coordinates[2]

        def crossproduct(x1,y1,x2,y2,x3,y3):
            return (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)
        
        d1 = crossproduct(x,y, x1,y1, x2,y2)
        d2 = crossproduct(x,y, x1,y1, x3,y3)
        d3 = crossproduct(x,y, x2,y2, x3,y3)

        pos = (d1<0) or (d2<0) or (d3<0)
        neg = (d1>0) or (d2>0) or (d3>0)

        return not (pos and neg)
    
    def area(self, mesh_points):
        x1,y1 = self._coordinates[0]
        x2,y2 = self._coordinates[1]
        x3,y3 = self._coordinates[2]

        self._area = 0.5 * np.abs((x1 - x3) * (y2 - y1) - (x1 - x2) * (y3 - y1))

    def midpoint(self, mesh_points):
        x1,y1 = self._coordinates[0]
        x2,y2 = self._coordinates[1]
        x3,y3 = self._coordinates[2]

        self._midpoint = [(x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3]
    
    def u_0(self, x, y):
        x1, y1 = self._midpoint
        vector = np.array([x1-x, y1-y])
        norm = np.linalg.norm(vector)
        self._u = np.exp(-(norm**2/0.01))
    
    def v(self):
        x, y = self._midpoint 
        self._v = np.array([y-0.2*x, -x])

    
        

    def g(u_i, u_ngh, norm, v):
        """
        u_i: amount of oil in cell i at time t_n
        u_ngh: amount of oil in cell ngh at time t_n
        norm: normal of cell i at edge e
        v: velocity field at edge e
        """
        if np.dot(norm) > 0:
            return self._u * np.dot(self._v , norm)
        else:
            return u_ngh * np.dot(self._v, norm)
    
def flux(u_i, u_ngh, norm, v, delta_t):
    return (-delta_t / self._area) * g(u_i, u_ngh, norm, v)

#def u_t(u_i, flux)
        
class Mesh:
    def __init__(self, msh):
        '''input: mesh
        reads in points and cells into lists that stores metadata'''
        self._points = [Point(msh.points, i) for i in range(len(msh.points))]
        self._cells = self._create_cells(msh.cells)
    
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
                all_cells.append(Cell.cell_factory(cell_type, idx, cell_points_id, orginal_cell_id))
                orginal_cell_id += 1
        return all_cells
    
    def store_coordinates(self):
        for cel in self._cells:
            if isinstance(cel, Cell):
                cel.get_point_coord(self._points)
    
    def find_neighbors_and_normals(self):
        """Find neighbors for cells"""
        for current_cell in self._cells:
            current_cell.store_neighbors(self._cells)
            if isinstance(current_cell, Triangle):
                current_cell.store_neighbors_scaled_normal(self._cells, self._points)
    
    def point_in_triangle(self, x,y):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                if cell.point_in_cell(x,y, self._points):
                    return cell
    
    def store_area(self):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                cell.area(self._cells, self._points)
    
    def store_midpoint(self):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                cell.midpoint(self._points)
        
    def initial_oil(self, x, y):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                cell.u_0(x,y)
    
    def flow_vector(self):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                cell.v()

    def __str__(self):
        """Print neighbor info"""
        return "\n".join(str(cell) for cell in self._cells)

