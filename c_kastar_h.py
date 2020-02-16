from pathlib import Path
path_parent = str(Path(Path(__file__).path_parent))
import sys
sys.path.append(path_parent + '\\f_utils')
sys.path.append(path_parent + '\\f_grid')

from c_opened import Opened
from c_astar import AStar
import u_grid

class KAStar_H:
    """
    ===========================================================================
     Description: KA* with Heuristic Improvements.
    ===========================================================================
    """
    
    def __init__(self, grid, start, goals):
       self.grid = grid
       self.start = start
       self.goals = goals
       
       self.counter_h = 0
       self.paths = dict()
       self.opened = set()
       self.closed = set()
       
       for goal in self._sorted_goals:
           astar = AStar(grid, start, goal)
           self.paths[goal] = astar.get_path()
           self.opened.update(set(astar.opened.get_nodes()))
           self.closed.update(astar.closed)
           
       
       
    def _sorted_goals(self):
        """
        =======================================================================
         Description: Return Sorted List of Goals by min distance from Start.
        =======================================================================
        """
        dic = dict()
        for goal in self.goals:
            dic[goal] = u_grid.manhattan_distance(self.grid, self.start, goal)
            self.counter_h += 1
        return [k for k, v in sorted(dic.items(), key=lambda item: item[1])]