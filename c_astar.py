from c_node import Node
from c_opened import Opened

import sys
sys.path.append('D:\\MyPy\\f_grid\\')
import u_grid


class AStar:
    """
    ===========================================================================
     Description: AStar
    ===========================================================================
     Methods:
    ---------------------------------------------------------------------------
    ===========================================================================
    """
    
    
    def __init__(self, grid, start, goal):
        """
        ===================================================================
         Description: A* Algorithm.
        ===================================================================
         Arguments:
        -------------------------------------------------------------------
            1. grid : Grid.
            2. start : int (Start's Id).
            3. goal : int (Goal's Id).
        ===================================================================
        """  
        self.start = start
        self.goal = goal
        self.grid = grid
        
        self.best = Node(start)
        self.best.g = 0
        
        self.closed = set()                     
        self.opened = Opened()
        self.opened.push(self.best)   
        
        self._run()
    
    
    def get_path(self):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Return: list of int (List of Nodes Idds or Empty List on No-Solution).
        =======================================================================
        """
        node = self.best
        if not node: return list()
        path = [node.idd]
        while (node.idd != self.start):
            node = node.father
            path.append(node.idd)
        path.reverse()
        return path            
        
    
    def _run(self):
        """
        =======================================================================
         Description: Run A* Algorithm.
        =======================================================================
        """
        while not (self.opened.is_empty()):
            self.best = self.opened.pop()
            self.closed.add(self.best)
            if (self.best.idd == self.goal):
                return
           
            self._expand()
        self.best = None
            
            
    def _expand(self):   
        """
        =======================================================================
         Description: Expand the Best Node's Children.
        =======================================================================
        """     
        row, col = u_grid.to_row_col(self.grid, self.best.idd)
        idds = u_grid.get_neighbors(self.grid, row, col)
        children = {Node(x) for x in idds} - self.closed      
        for child in sorted(children):
            if self.opened.contains(child):
                child = self.opened.get(child)
            g_new = self.best.g + child.w
            if child.g <= g_new:
                continue
            self._update_node(child,self.best,g_new)
            if not self.opened.contains(child):
                self.opened.push(child)
            
            
    def _update_node(self, node, father, g):
        """
        =======================================================================
         Description: Update Node.
        =======================================================================
         Attributes:
        -----------------------------------------------------------------------
            1. node : Node (node to update)
            2. father : Node
            3. g : int
        =======================================================================
        """
        node.father = father
        node.g = g
        node.h = u_grid.manhattan_distance(self.grid,node.idd,self.goal)
        node.f = node.g + node.h        

    
"""
===============================================================================
===============================================================================
=========================  Tester  ============================================
===============================================================================
===============================================================================
"""
def tester():
    
    import random
    import sys
    
    sys.path.append('D:\\MyPy\\f_utils')
    import u_tester
    import u_random
            
    def tester_run():
     
        p0 = True
        for i in range(1000):
            n = u_random.get_random_int(3,10)
            grid = u_grid.gen_symmetric_grid(n)
            idds_valid = u_grid.get_valid_idds(grid)
            random.shuffle(idds_valid)
            start = idds_valid[0]
            goal = idds_valid[1]
            astar = AStar(grid,start,goal)
            len_optimal = u_grid.manhattan_distance(grid,start,goal)+1
            if len(astar.get_path()) != len_optimal:
                p0 = False
                
        p1 = True
        for i in range(1000):
            n = u_random.get_random_int(5,10)
            grid = u_grid.gen_obstacles_grid(n,30)
            idds_valid = u_grid.get_valid_idds(grid)
            random.shuffle(idds_valid)
            start = idds_valid[0]
            goal = idds_valid[1]
            astar = AStar(grid,start,goal)
            dic_g = u_grid.to_dic_g(grid,start)
            len_optimal = dic_g.get(goal)
            if len_optimal:
                p1 = len_optimal+1 == len(astar.get_path())
            if not p1:
                break
            
        u_tester.run([p0,p1])
    
    
    def tester_get_path():
        
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goal = 8
        astar = AStar(grid, start, goal)
        astar_test = astar.get_path()
        astar_true = [0,3,6,7,8]
        p0 = astar_test == astar_true
        
        u_tester.run([p0])
        
    u_tester.print_start(__file__)
    tester_run()
    tester_get_path()
    u_tester.print_finish(__file__)


if __name__ == '__main__':
    tester()
