import meshio
from abc import ABC, abstractmethod
import numpy as np


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
            if self._original_index != other_cell._original_index: #ensures diff. cells
                shared_points = set(self._cell_points_id) & set(other_cell._cell_points_id) #hashes for pair points of cells
                if isinstance(other_cell, Line) and len(shared_points) == 1: #if more or equal to 1 shared point, the other cell is a neighbor
                    self._neighbors.append(other_cell._original_index) #adds to list
                    self._is_boundary = True
                    
                elif len(shared_points) == 2:
                    self._neighbors.append(other_cell._original_index) #adds to list

    def __str__(self): #prints info
        return f"Line {self._original_index}, Boundary: {self._is_boundary}, Neighbors: {self._neighbors}"

class Triangle(Cell): #triangle class, parent class: cell
    #finds neighbors and corresponding scaled normal vectors, and stores in list

    def store_neighbors(self, all_cells):
        for other_cell in all_cells: #checks all cells in mesh
            if self._original_index != other_cell._original_index: #checks diff. cell
                shared_points = set(self._cell_points_id) & set(other_cell._cell_points_id) #hashes for pair points of cells
                if len(shared_points) == 2: #if equal to 2 shared points, the othe cell is a neighbor
                    shared_points=list(shared_points)
                    self._neighbors.append({other_cell._original_index: shared_points}) #adds to list

                    if len(self._neighbors) == 3:
                        break
        
    def __str__(self): #prints info
        return f"Triangle {self._original_index}, Oil: {self.get_amount_of_oil()} Normals:{self._scaled_normals} Neighbors:{self._neighbors} Velocity:{self.get_flowfield()}"

        
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
        for cell in self._cells:
            
            cell.get_point_coord(self._points)
    
    def find_neighbors(self):
        """Find neighbors for cells"""
        for cell in self._cells:
            
            cell.store_neighbors(self._cells)
