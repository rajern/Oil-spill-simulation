import meshio
from abc import ABC, abstractmethod
import numpy as np

class point:
    '''class for point of x and y cord.
    input: all the points in the mesh, cell points index'''
    def __init__(self, points, pointindex):
        self._point_index = pointindex
        self._x, self._y = points[pointindex][:2] #2D mesh

    def __repr__(self): #Returning point desc.
        return f"Point(index={self._point_index}, x={self._x:.2f}, y={self._y:.2f})"
    

class cell(ABC):
    '''class for cells
    input: cells id, cell points id, the orginal cell id'''
    def __init__(self, cell_index, cell_points_id, original_index):
        self._cell_index = cell_index
        self._original_index = original_index  #
        self._cell_points_id = cell_points_id
        self._neighbors = [] #empty list for neigbor cells to be stored
        self._is_boundary = False #boundary statement is false by default
        self._area = 0

    @abstractmethod #all types of cell classes must have this func.
    def store_neighbors(self, all_cells):
        pass


    @staticmethod #cell factory for all types of cells 
    def cell_factory(cell_type, cell_index, cell_points_id, original_index):
        if cell_type.lower() == "triangle":
            return triangle(cell_index, cell_points_id, original_index)
        elif cell_type.lower() == "line":
            return line(cell_index, cell_points_id, original_index)
        else:
            raise ValueError(f"Unknown cell type: {cell_type}")
        
    def get_point_cord(self, point_id, mesh_points):
        point_obj = mesh_points[point_id]
        return point_obj._x, point_obj._y
        

class line(cell): #line class, parent class: cell
    #finds neighbors and stores in list
    def store_neighbors(self, all_cells):
        for other_cell in all_cells: #checks all cells in mesh
            if self._cell_index != other_cell._cell_index: #ensures diff. cells
                shared_points = set(self._cell_points_id) & set(other_cell._cell_points_id) #hashes for pair points of cells
                if isinstance(other_cell, line) and len(shared_points) == 1: #if more or equal to 1 shared point, the other cell is a neighbor
                    self._neighbors.append(other_cell._cell_index) #adds to list
                    self._is_boundary = True
                    
                elif len(shared_points) == 2:
                    self._neighbors.append(other_cell._cell_index) #adds to list

    def __str__(self): #prints info
        return f"Line {self._original_index}, Boundary: {self._is_boundary}, Neighbors: {self._neighbors}"


class triangle(cell): #triangle class, parent class: cell
    #finds neighbors and stores in list
    def store_neighbors(self, all_cells):
        for other_cell in all_cells: #checks all cells in mesh
            if self._cell_index != other_cell._cell_index: #checks diff. cell
                shared_points = set(self._cell_points_id) & set(other_cell._cell_points_id) #hashes for pair points of cells
                if len(shared_points) == 2: #if equal to 2 shared points, the othe cell is a neighbor
                    self._neighbors.append(other_cell._cell_index) #adds to list
                    
                    #boundary check
                    if isinstance(other_cell, line): #checks if neighbor cell is a line
                        self._is_boundary = True
    
    def __str__(self): #prints info
        return f"Triangle {self._original_index}, Boundary: {self._is_boundary}, Neighbors: {self._neighbors}, Area: {self._area:.2f}"
    
    def point_in_cell(self, x, y, mesh_points):
        p1 = self._cell_points_id[0] #saves point
        p2 = self._cell_points_id[1]
        p3 = self._cell_points_id[2]

        x1,y1 = self.get_point_cord(p1, mesh_points)
        x2,y2 = self.get_point_cord(p2, mesh_points)
        x3,y3 = self.get_point_cord(p3, mesh_points)

        def crossproduct(x1,y1,x2,y2,x3,y3):
            return (x2-x1)*(y3-y1) - (y2-y1)*(x3-x1)
        
        d1 = crossproduct(x,y, x1,y1, x2,y2)
        d2 = crossproduct(x,y, x1,y1, x3,y3)
        d3 = crossproduct(x,y, x2,y2, x3,y3)

        pos = (d1<0) or (d2<0) or (d3<0)
        neg = (d1>0) or (d2>0) or (d3>0)

        return not (pos and neg)
    
    def area(self, mesh_points):
        p1 = self._cell_points_id[0] #saves point
        p2 = self._cell_points_id[1]
        p3 = self._cell_points_id[2]

        x1,y1 = self.get_point_cord(p1, mesh_points)
        x2,y2 = self.get_point_cord(p2, mesh_points)
        x3,y3 = self.get_point_cord(p3, mesh_points)

        self._area = 0.5 * np.abs((x1 - x3) * (y2 - y1) - (x1 - x2) * (y3 - y1))

    def midpoint(self, mesh_points):
        p1 = self._cell_points_id[0]
        p2 = self._cell_points_id[1]
        p3 = self._cell_points_id[2]

        x1,y1 = self.get_point_cord(p1, mesh_points)
        x2,y2 = self.get_point_cord(p2, mesh_points)
        x3,y3 = self.get_point_cord(p3, mesh_points)

        return (x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3

        
class Mesh:
    def __init__(self, msh):
        '''input: mesh
        reads in points and cells into lists that stores metadata'''
        self._points = [point(msh.points, i) for i in range(len(msh.points))]
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
                all_cells.append(cell.cell_factory(cell_type, idx, cell_points_id, orginal_cell_id))
                orginal_cell_id += 1
        return all_cells
    
    def find_neighbors(self):
        """Find neighbors for cells"""
        for current_cell in self._cells:
            current_cell.store_neighbors(self._cells)
    
    def point_in_triangle(self, x,y):
        for cell in self._cells:
            if isinstance(cell, triangle):
                if cell.point_in_cell(x,y, self._points):
                    return cell
    
    def store_area(self):
        for cell in self._cells:
            if isinstance(cell, triangle):
                cell.area(self._cells, self._points)
    
    def store_midpoint(self):
        for cell in self._cells:
            if isinstance(cell, triangle):
                cell.midpoint(self._points)

    def __str__(self):
        """Print neighbor info"""
        return "\n".join(str(cell) for cell in self._cells)

