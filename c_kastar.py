import sys
sys.path.append('D:\\MyPy\\f_grid')
sys.path.append('D:\\MyPy\\f_utils')

import u_grid
import u_set
from c_node import Node
from c_opened import Opened

class KAStar:
    
    
    def __init__(self, grid, start, goals):
        """
        =======================================================================
         Description: KA* Algorithm.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. grid : Grid.
            2. start : int (Start Idd).
            3. goals : set of int (Goal Idd).
        =======================================================================
        """  
        self.start = start
        self.goals = goals
        self.grid = grid
        self.counter_h = 0
        
    
    def run(self):
        """
        =======================================================================
         Description: Run KA* Algorithm.
        =======================================================================
        """
        if not (self.start or self.goals): return
        
        self.goals_active = set(self.goals) 
        self.closed = set()                     
        self.opened = Opened()
        self.counter_h = 0
               
        self.best = Node(self.start)
        self._update_node(self.best,g=0)        
        self.opened.push(self.best)   
        
        while (self.goals_active and not self.opened.is_empty()):
            self.best = self.opened.pop()
            self.closed.add(self.best)
            if (self.best.idd in self.goals_active):
                self.goals_active.remove(self.best.idd)
                if not self.goals_active: 
                    return
                self._update_opened()     
            self._expand_best()
            
            
    def get_path(self, goal):
        """
        =======================================================================
         Description: Return Optimal Path from Start to Goal.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. goal : Node
        =======================================================================
         Return: list of Node (Empty List on No-Solution).
        =======================================================================
        """            
        node = u_set.get(self.closed, Node(goal))
        if not node: return list()
        path = [node.idd]
        while (node.idd != self.start):
            node = node.father
            path.append(node.idd)
        path.reverse()        
        return path
            
            
    def _update_opened(self):
        """
        =======================================================================
         Description: Update h of Opened Nodes (after removing active goal).
        =======================================================================
        """
        for node in self.opened.get_nodes():
            node.h = self._get_min_h(node)
            node.f = node.g + node.h
            
        
    def _expand_best(self):   
        """
        ===================================================================
         Description: Expand the Best Node's Children.
        ===================================================================
        """     
        row, col = u_grid.to_row_col(self.grid, self.best.idd)
        idds = u_grid.get_neighbors(self.grid, row, col)
        children = {Node(x) for x in idds} - self.closed      
        for child in sorted(children):
            if self.opened.contains(child):
                child = self.opened.get(child)
            g_new = self.best.g + child.w
            # Already in Opened with best g 
            if child.g <= g_new:
                continue
            self._update_node(child, g_new)
            self.opened.push(child)
            
            
    def _update_node(self, node, g):
        """
        =======================================================================
         Description: Update Node.
        =======================================================================
         Attributes:
        -----------------------------------------------------------------------
            1. node : Node (Node to update).
            2. g : int
        =======================================================================
        """
        if not node == self.best:
            node.father = self.best
        node.g = g
        node.h = self._get_min_h(node)
        node.f = node.g + node.h


    def _get_min_h(self, node):
        """
        =======================================================================
         Description: Calc h toward the Active Goals and Return the Minimum.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. node : Node
        =======================================================================
         Return: float (Minimum h toward the Active Goals).
        =======================================================================
        """
        h = float('Infinity')
        for goal in self.goals_active:
            h = min(h, self._get_manhattan_distance(node,goal))
        return h
        
    
    def _get_manhattan_distance(self, node, goal):
        """
        =======================================================================
         Description: Return Manhattan Distance between Node and Goal.
        =======================================================================
         Arguments:
        -----------------------------------------------------------------------
            1. node : Node.
            2. goal : int (Goal's Id).
        =======================================================================
         Return: float (Manhattan Distance between Node and Goal).
        =======================================================================
        """
        self.counter_h += 1
        return u_grid.manhattan_distance(self.grid, node.idd, goal)        

    
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
    
    def tester_get_manhattan_distance():
        
        grid = u_grid.gen_symmetric_grid(3)
        kastar = KAStar(grid, None, None)
        node = Node(0)
        goal = 8
        dist_test = kastar._get_manhattan_distance(node, goal)
        dist_true = u_grid.manhattan_distance(grid,node.idd,goal)
        p0 = dist_test == dist_true
        
        u_tester.run([p0])
        
    
    def tester_get_min_h():
        
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {2,3}
        kastar = KAStar(grid, start, goals)
        kastar.run()
        kastar.goals_active = goals
        h_test = kastar._get_min_h(Node(start))
        h_true = 1
        p0 = h_test == h_true
        
        u_tester.run([p0])
        
        
    def tester_update_node():
        
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {1}
        kastar = KAStar(grid, start, goals)
        kastar.run()
        
        node = Node(0)
        kastar._update_node(node, 1)
        p0 = (node.father == kastar.best) and (node.g == 1)
        p0 *= (node.h == kastar._get_min_h(node)) and (node.f == node.g+node.h)
        
        u_tester.run([p0])
        
        
    def tester_expand_best():
        
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {1}
        kastar = KAStar(grid, start, goals)
        kastar.run()
        
        p0 = not (kastar.opened.contains(Node(5)) or kastar.opened.contains(Node(7)))
        kastar.best = Node(8)
        kastar.best.g = 1
        kastar._expand_best()
        p0 *= (kastar.opened.contains(Node(5)) and kastar.opened.contains(Node(7)))
        u_tester.run([p0])
        
    
    def tester_update_opened():
        
        grid = u_grid.gen_symmetric_grid(3)
        start = 0
        goals = {1}
        kastar = KAStar(grid, start, goals)
        kastar.run()
        kastar.goals_active = {8}
        kastar._update_opened()
        d_test = { node.idd:node.h for node in kastar.opened.get_nodes() }
        d_true = {node.idd:u_grid.manhattan_distance(grid,node.idd,8) for node in kastar.opened.get_nodes()}
        p0 = d_test == d_true
        
        u_tester.run([p0])
        
        
    def tester_run():         
        
        from c_astar import AStar
        
        p0 = True
        for i in range(1000):
            n = u_random.get_random_int(5,10)
            k = u_random.get_random_int(2,10)
            if k >= n*n: continue
            grid = u_grid.gen_symmetric_grid(n)
            idds = u_grid.get_valid_idds(grid)
            random.shuffle(idds)
            start = idds[0]
            goals = idds[1:k+1]
            kastar = KAStar(grid, start, goals)
            kastar.run()
            for goal in goals:
                path_test = kastar.get_path(goal)
                astar = AStar(grid, start, goal)
                path_true = astar.get_path()
                p0 *= len(path_test) == len(path_true)
                if not p0: break
            if not p0: break
        
        p1 = True
        for i in range(1000):
            n = u_random.get_random_int(5,10)
            k = u_random.get_random_int(2,10)
            if k >= n*n: continue
            grid = u_grid.gen_obstacles_grid(n, 10)
            idds = u_grid.get_valid_idds(grid)
            random.shuffle(idds)
            start = idds[0]
            goals = idds[1:k+1]
            kastar = KAStar(grid, start, goals)
            kastar.run()
            for goal in goals:
                path_test = kastar.get_path(goal)
                astar = AStar(grid, start, goal)
                path_true = astar.get_path()
                p1 *= len(path_test) == len(path_true)
                if not p1: break
            if not p1: break
            
        u_tester.run([p0,p1])
            
            
    def tester_get_path():
        grid = u_grid.gen_symmetric_grid(4)
        start = 0
        goal = 12
        astar = KAStar(grid,start,{goal})
        astar.run()
        optimal_path = [0,4,8,12]
        p1 = astar.get_path(goal) == optimal_path
        
        grid = u_grid.gen_symmetric_grid(4)
        grid[1][1] = -1
        grid[2][1] = -1
        start = 8
        goal = 10
        astar = KAStar(grid,start,{goal})
        astar.run()
        optimal_path = [8,12,13,14,10]
        p2 = astar.get_path(goal) == optimal_path
        
        p3 = True
        for i in range(1000):
            n = u_random.get_random_int(4,4)
            grid = u_grid.gen_symmetric_grid(n)
            idds_valid = u_grid.get_valid_idds(grid)
            random.shuffle(idds_valid)
            start = idds_valid[0]
            goals = idds_valid[1:3]
            kastar = KAStar(grid,start,goals)
            kastar.run()
            for goal in goals:
                len_optimal = u_grid.manhattan_distance(grid,start,goal)+1
                if len(kastar.get_path(goal)) != len_optimal:
                    p3 = False
                    print('start={0}'.format(start))
                    print('goal={0}'.format(goals))
                    print('grid:')
                    for row in range(grid.shape[0]):
                        li = list()
                        for col in range(grid.shape[1]):
                            li.append(grid[row][col])
                        li = [str(x) for x in li]
                        print(','.join(li))
                    print('goal[{0}]: {1}'.format(goal,kastar.get_path(goal)))            
        
        fname = sys._getframe().f_code.co_name[7:]
        if (p1 and p2 and p3):        
            print('OK: {0}'.format(fname))
        else:
            print('Failed: {0}'.format(fname))  
    
    u_tester.print_start(__file__)
    tester_get_manhattan_distance()
    tester_get_min_h()
    tester_update_node()
    tester_expand_best()
    tester_update_opened()
    tester_run()
    u_tester.print_finish(__file__)       
    
    
if __name__ == '__main__':
    tester()
