import heapq
import pygame

class PriorityQueue:
    def __init__(self):
        self.count = 0

        self.queue = []
        heapq.heapify(self.queue)

    def append(self, node):
        self.count += 1
        node.curr_square.frontier = True
        push_node = (node.score, self.count, node)
        heapq.heappush(self.queue, push_node)

    def pop(self):
        node = heapq.heappop(self.queue)
        return node

    def remove(self, rem_node):
        idx_cnt = 0
        for (score, count, node) in self.queue:
            if node.name == rem_node.name:
                break
            idx_cnt += 1
        temp_queue = self.queue[:idx_cnt] + self.queue[idx_cnt+1:]
        self.queue = temp_queue
        self.count -= 1

    def __contains__(self, node):
        return node.name in [node[-1].name for node in self.queue]
    
    def __iter__(self):
        return iter([node for (_,_,node) in self.queue])

class explored_set:
    def __init__(self):
        self.explored = set()

    def add(self, node):
        node.curr_square.explored = True
        self.explored.add(node.name)

    def __contains__(self, key):
        return key.name in self.explored

class square:
    def __init__(self, col, row, screen, color, columns, rows, show_steps, start, end, grid):
        self.col = col
        self.row = row
        self.pos = (self.row, self.col)
        height, width = screen.get_size()
        self.w = width / columns
        self.h = height / rows
        self.base_color = color
        self.color = color
        self.screen = screen
        self._moveto = True
        self._frontier = False
        self._explored = False
        self.show_steps = show_steps

        self.start = start
        self.end = end
        self.columns = columns
        self.rows = rows

        self.grid = grid

    def show(self, filled):
        ''' Draws the rectangle, if filled is False, the rectangle will be empty, if True, it will fill in '''
        pygame.draw.rect(self.screen, self.color, (self.col*self.w, self.row*self.h, self.w, self.h), filled)
        pygame.display.update()

    @property
    def moveto(self):
        return self._moveto

    @moveto.setter
    def moveto(self, val):
        if val == False:
            self.color = (255,255,255)
            self._moveto = val
            self.show(0)
        else:
            self.color = (0,0,0)
            self.show(0)
            self.color = self.base_color
            self._moveto = val
            self.show(1)

    @property
    def frontier(self):
        return self._frontier

    @frontier.setter
    def frontier(self, val):
        if (self.row, self.col) != self.start and (self.row, self.col) != self.end:
            if val == True and self.explored == False:
                self.color = (255,255,0)
                self._frontier = val
                if self.show_steps:
                    self.show(0)

    @property
    def explored(self):
        return self._explored

    @explored.setter
    def explored(self, val):
        if (self.row, self.col) != self.start and (self.row, self.col) != self.end:
            if val == True:
                self.color = (0,71,171)
                self._explored = val
                if self.show_steps:
                    self.show(0)

class Node:
    def __init__(self, curr, end, scoring,path = None):
        if path is None:
            self.path = [(curr.pos)]
        else:
            self.path = path
        self.curr_square = curr
        self.name = (curr.pos)
        self.is_goal = ((curr.pos) == end)
        self.goal = end
        self.scoring = scoring
        self.score = scoring(self)
        #self.score = len(self.path) + heuristic((curr.pos), end)


    def generate_neighbors(self):
        pos = (self.curr_square.row, self.curr_square.col)
        neighbors = []
        curr_row = pos[0]
        curr_col = pos[1]
        for row_mod in [-1,0,1]:
            for col_mod in [-1, 0, 1]:
                if row_mod == 0 and col_mod == 0:
                    continue
                if curr_row-row_mod in range(self.curr_square.rows):
                    if curr_col-col_mod in range(self.curr_square.columns):
                        if self.curr_square.grid[curr_row-row_mod][curr_col-col_mod].moveto:
                            path = self.path.copy()
                            path.append((curr_row-row_mod, curr_col-col_mod))
                            child_node = Node(self.curr_square.grid[curr_row-row_mod][curr_col-col_mod], self.goal, self.scoring, path)
                            neighbors.append(child_node)
        return neighbors

    def __lt__(self, other):
        return self.score < other.score


