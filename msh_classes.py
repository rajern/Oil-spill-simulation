import meshio as m
from abc import ABC, abstractmethod

class point:
    '''class for point of x and y cord.
    input: all the points in the mesh, cell points index '''
    def __init__(self, points, pointindex):
        self._point_index = pointindex
        self._x, self._y = points[pointindex][:2] #2D mesh

    
    def __repr__(self): #Returning point desc.
        return f"Point(index={self._point_index}, x={self._x:.2f}, y={self._y:.2f})"
    

class line(cell): #line class, parent class: cell
    #finds neighbors and stores in list
    def store_neighbors(self, all_cells):
        for other_cell in all_cells: #checks all cells in mesh
            if self._cell_index != other_cell._cell_index: #ensures diff. cells
                shared_points = set(self._cell_points_id) & set(other_cell._cell_points_id) #hashes for pair points of cells
                if len(shared_points) >= 1: #if more or equal to 1 shared point, the other cell is a neighbor
                    self._neighbors.append(other_cell._cell_index) #adds to list
                    
                    #boundary check
                    if isinstance(other_cell, line): #checks if neighbor cell is a line
                        self._is_boundary = True

    def __str__(self): #prints info
        return f"Line {self._original_index}, Boundary: {self._is_boundary}, Neighbors: {self._neighbors}"


class triangle(cell): #triangle class, parent class: cell
    #finds neighbors and stores in list
    def store_neighbors(self, all_cells):
        for other_cell in all_cells: #checks all cells in mesh
            if self._cell_index != other_cell._cell_index: #checks diff. cell
                shared_points = set(self._cell_points_id) & set(other_cell._cell_points_id) #hashes for pair points of cells
                if len(shared_points) >= 2: #if more or equal to 2 shared points, the othe cell is a neighbor
                    self._neighbors.append(other_cell._cell_index) #adds to list
                    
                    #boundary check
                    if isinstance(other_cell, line): #checks if neighbor cell is a line
                        self._is_boundary = True
    
    def __str__(self): #prints info
        return f"Triangle {self._original_index}, Boundary: {self._is_boundary}, Neighbors: {self._neighbors}"


class mesh:
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
    
    def __str__(self):
        """Print neighbor info"""
        return "\n".join(str(cell) for cell in self._cells)
