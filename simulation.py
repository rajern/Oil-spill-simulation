from msh_classes import *

def flux(u_i, u_ngh, normal, v):
    """
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
        
    def __init__(self):
        self._midpoint = [] 
        self._area = 0
        self._u = 0
        self._v = []
        self._scaled_normals = []

class Sim_Trianle(Triangle, Sim_Cell):
    
    
    def scaled_normals(self):
        pointer1 = [0,1,2]
        pointer2 = [1,2,0]
        midpoint = self._midpoint

        for i,j in zip(pointer1,pointer2):
            p_j = self._coordinates[j]
            p_i = self._coordinates[i]
            e_vector = np.subtract(p_j, p_i)
            normal = [e_vector[1], -e_vector[0]] #[e[1], -e[0]] = [dy, -dx]
            orthonormal = normal / np.linalg.norm(normal)

            check_vector = np.subtract(p_i, midpoint)
            scaled_normals = orthonormal * np.linalg.norm(e_vector)
            if np.dot(orthonormal,check_vector)<0:
                scaled_normals = np.flip(scaled_normals)
            
            for ngh in self._neighbors:
                for neighbor_cell, shared_points in ngh.items():
                    if np.isin(self._cell_points_id[i], shared_points) and np.isin(self._cell_points_id[j], shared_points):
                        # Store the scaled normal vector with the neighbor cell as the key
                        self._scaled_normals.append({neighbor_cell: scaled_normals})
                        print({neighbor_cell: scaled_normals})  # print the scaled normal vector for debugging

            


    def __str__(self): #prints info
        return f"Triangle {self._original_index}, Oil: {self.get_amount_of_oil()} Normals:{self._scaled_normals} Neighbors:{self._neighbors} Velocity:{self.get_flowfield()}"
    
    def area(self):
        x1,y1 = self._coordinates[0]
        x2,y2 = self._coordinates[1]
        x3,y3 = self._coordinates[2]

        self._area = 0.5 * np.abs((x1 - x3) * (y2 - y1) - (x1 - x2) * (y3 - y1))

    def midpoint(self):
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

    def up(self, delta_t, mesh_cells):
        up = 0

        for ngh_data in self._scaled_normals:
            for ngh_cell_id, scaled_normal in ngh_data.items():
                ngh_cell_id = int(ngh_cell_id)
                if isinstance(mesh_cells[ngh_cell_id], Line):
                    continue

                v = 0.5 * (self._v + mesh_cells[ngh_cell_id]._v)  
                flux_value = flux(self._u, mesh_cells[ngh_cell_id]._u, scaled_normal, v)
                up -= delta_t / self._area * flux_value
            
        self._u = self._u + up


class Sim_Mesh:
    def store_area(self):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                
                cell.area()
    
    def store_midpoint(self):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                
                cell.midpoint()
        
    def initial_oil(self, x, y):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                
                cell.u_0(x,y)
    
    def flow_vector(self):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                
                cell.v()
    
    def update_oil(self, delta_t):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                
                cell.up(delta_t, self._cells)
    
    def normal(self):
        for cell in self._cells:
            if isinstance(cell, Triangle):
                
                cell.scaled_normals()