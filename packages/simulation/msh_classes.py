import meshio
from abc import ABC, abstractmethod
"""
This file provides basic definition and storing of the classes Point, Cell, Line and Triangle.
"""

class Point:
    """
    A simple class that stores the points id's and their coordinates.
    """
    def __init__(self, points, point_index):
        """
        Stores the points id's and their coordinates in the Point class.

        Paramteres: 
        points: list of point coordinates from mesh
        point_index: index of the points

        """
        self._point_index = point_index
        self._x, self._y = points[point_index][:2] #2D mesh

    def __repr__(self): #Returning point desc.
        return f"Point(index={self._point_index}, x={self._x:.2f}, y={self._y:.2f})"
    

class Cell(ABC):
    """
    A parent class for all Cells.
    """
    def __init__(self, cell_index, cell_points_id, original_index):
        """
        Stores the cell id, cell points id, original cell id, neighbours and coordinates in the Cell class.

        Paramteres:
        cell_index: index of the cell
        cell_points_id: id of the cell points
        original_index: original index of the cell (same as cell_index)

        """
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
        """
        Factory method for creating cells.
        
        Parameters:
        cell_type: type of cell (either triangle or line)
        cell_index: index of the cell
        cell_points_id: id of the cell points
        original_index: original index of the cell (same as cell_index)

        Returns a cell object of the correct type consisting of cell_id and cell_points_id.
        """
        if cell_type.lower() == "triangle":
            return Triangle(cell_index, cell_points_id, original_index)
        elif cell_type.lower() == "line":
            return Line(cell_index, cell_points_id, original_index)
        else:
            raise ValueError(f"Unknown cell type: {cell_type}")
        
    def point_coord(self, point_id, mesh_points): 
        """
        Function for converting points to x-, y- coordinates

        Parameters:
        point_id: id of the point
        mesh_points: list of points in mesh

        Returns x- and y-coordinates of the point
        """
        point_obj = mesh_points[point_id]
        return point_obj._x, point_obj._y
    
    def get_point_coord(self, mesh_points):
        """
        Function for storing the x-, y-coordinates of the cell points.
        Uses the function point_coord to store the x-, y-coordinates of the cell points in the list _coordinates
        
        Parameters:
        mesh_points: list of points in mesh
        """

        self._coordinates = [self.point_coord(point_id, mesh_points) for point_id in self._cell_points_id]
        

class Line(Cell): 
    """
    Child class of the Cell class that stores the Line Cells.
    """
    def store_neighbors(self, all_cells):
        """
        A function that stores the neighbors of the Line Cells. 
        It checks if cells of type Line shares points with other Line cells, and if so, stores them in the list _neighbors.

        Parameters:
        all_cells: list of all cells in the mesh
        """
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

class Triangle(Cell): 
    """
    Child class of the Cell class that stores the Triangle Cells.
    """

    def store_neighbors(self, all_cells):
        """
        A function that stores the neighbors of the Triangle Cells.
        It checks if cells of type Triangle shares points with other Triangle cells, and if so, stores them in the list _neighbors.
        
        Parameters:
        all_cells: list of all cells in the mesh
        """
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
    """
    A class that stores the mesh data and creates the mesh."""
    def __init__(self, msh):
        """
        Stores the mesh data in a list of points and a list of cells.
        The mesh-point data is stored in the Point class and the mesh-cells are created in the _create_cells function.
        
        Parameters:
        msh: mesh file
        """
        self._points = [Point(msh.points, i) for i in range(len(msh.points))]
        self._cells = self._create_cells(msh.cells)
    
    def _create_cells(self, mesh_cells):
        """
        A function that creates the cells in the mesh.
        The function loops through the mesh-cells and creates the cells using the cell_factory function
        and stores them in the Cell class.
        
        Parameters:
        mesh_cells: list of cells in the mesh        
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
                all_cells.append(Cell.cell_factory(cell_type, idx, cell_points_id, orginal_cell_id))
                orginal_cell_id += 1
        return all_cells
    
    def store_coordinates(self):
        """
        A function that stores the x-, y-coordinates of the cell points in the _points list.

        Uses the get_point_coord function.
        """
        for cell in self._cells:
            
            cell.get_point_coord(self._points)
        
        print("Coordinates stored in all cells")
    
    def find_neighbors(self):
        """
        A function that stores the neighbors of the cells in the mesh in the _cells list.
        Uses the store_neighbors function.
        """
        for cell in self._cells:                
            if isinstance(cell, Triangle):
                cell.store_neighbors(self._cells)
            
        print("Neighbors for cells computed")