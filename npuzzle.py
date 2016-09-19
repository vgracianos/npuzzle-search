from time import time
from heapq import *
from random import randint
from collections import deque
#import svgwrite

# timer decorator
def print_timing(func):
    def wrapper(*arg):
        print 'Running %s algorithm...' % func.func_name
        t1 = time()
        res = func(*arg)
        t2 = time()
        print 'Found a solution costing %d steps in %0.4f seconds\n' % (len(res), t2 - t1)
        return res
    return wrapper

class npuzzle:
    # build a NxN puzzle.
    def __init__(self, N, steps = 100):
        self.N = N
        self.goal_state = range(1, N**2)
        self.goal_state.append(0)
        self.init_state = self.genState(steps)

    # generate a random state.
    def genState(self, steps):
        state = self.goal_state[:]
        last_state = state
        for i in xrange(steps):
            succ_list = self.successors(state)
            state = succ_list[randint(0, len(succ_list) - 1)][1]
        return state

    # return a list containing (action, state) pairs.
    def successors(self, state):
        blank = state.index(0)
        y, x  = blank / self.N, blank % self.N
        actions = dict([((1, 0), 'v'), ((-1, 0), '^'),
                        ((0, 1), '>'), ((0, -1), '<')])
        succ_list = []
        for dy, dx in actions.keys():
            new_x, new_y = x + dx, y + dy
            if new_x >= 0 and new_x < self.N and new_y >= 0 and new_y < self.N:
                new_state, new_blank = state[:], new_y * self.N + new_x
                new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]
                succ_list.append((actions[(dy, dx)], new_state))
        return succ_list

    # build the solution based on the chain of parent nodes
    def buildSolution(self, node):
        solution = []
        while node[3] != None:
            solution.append(node[4])
            node = node[3]
        return solution[::-1]

    # solve the puzzle using breadth-first search.
    @print_timing
    def breadth(self):
        # f and h are unused here.
        # node = (f, g, h, parent, action, state)
        open_list   = deque([(0, 0, 0, None, None, self.init_state)])
        closed_list = dict()
        while open_list:
            node = open_list.popleft()
            if node[5] == self.goal_state:
                return self.buildSolution(node)
            closed_list[tuple(node[5])] = True
            for succ in self.successors(node[5]):
                if tuple(succ[1]) not in closed_list:
                    open_list.append((0, node[1] + 1, 0, node, succ[0], succ[1]))
        return []

    # solve the puzzle using iterative deepening search.
    @print_timing
    def ids(self):
        depth = 0
        while True:
            # f and h are unused here.
            # node = (f, g, h, parent, action, state)
            open_list   = deque([(0, 0, 0, None, None, self.init_state)])
            closed_list = dict()
            depth += 1
            while open_list:
                node = open_list.pop()
                if node[5] == self.goal_state:
                    return self.buildSolution(node)
                if node[1] + 1 > depth:
                    continue
                closed_list[tuple(node[5])] = node[1]
                for succ in self.successors(node[5]):
                    tstate = tuple(succ[1])
                    if tstate not in closed_list:
                        open_list.append((0, node[1] + 1, 0, node, succ[0], succ[1]))
                    elif closed_list[tstate] > node[1] + 1: # reopens the node
                        del closed_list[tstate]
                        open_list.append((0, node[1] + 1, 0, node, succ[0], succ[1]))
        return []

    # manhattan distance heuristic for A* search.
    def manhattan(self, state):
        distance = 0
        for i in xrange(self.N**2):
            j = self.goal_state.index(state[i])
            yi, xi = i / self.N, i % self.N
            yj, xj = j / self.N, j % self.N
            distance += abs(xi - xj) + abs(yi - yj)
        return distance

    # solve the puzzle using A* search.
    @print_timing
    def astar(self):
        # node = (f, g, h, parent, action, state)
        open_list   = [(0, 0, 0, None, None, self.init_state)]
        closed_list = dict()
        while open_list:
            node = heappop(open_list)
            # this is necessary as there is no decrease_key available.
            if tuple(node[5]) in closed_list:
                continue
            if node[5] == self.goal_state:
                return self.buildSolution(node)
            closed_list[tuple(node[5])] = True
            for succ in self.successors(node[5]):
                if tuple(succ[1]) not in closed_list:
                    g = node[1] + 1
                    h = self.manhattan(succ[1])
                    heappush(open_list, (g + h, g, h, node, succ[0], succ[1]))
        return []

    # solve the puzzle using uniform cost search.
    @print_timing
    def ucs(self):
        # node = (f, g, h, parent, action, state)
        open_list   = [(0, 0, 0, None, None, self.init_state)]
        closed_list = dict()
        while open_list:
            node = heappop(open_list)
            # this is necessary as there is no decrease_key available.
            if tuple(node[5]) in closed_list:
                continue
            if node[5] == self.goal_state:
                return self.buildSolution(node)
            closed_list[tuple(node[5])] = True
            for succ in self.successors(node[5]):
                if tuple(succ[1]) not in closed_list:
                    g = node[1] + 1
                    h = self.manhattan(succ[1])
                    heappush(open_list, (g, g, 0, node, succ[0], succ[1]))
        return []
                
    # solve the puzzle using greedy search (manhattan distance).
    @print_timing
    def greedy(self):
        # node = (f, g, h, parent, action, state)
        open_list   = [(0, 0, 0, None, None, self.init_state)]
        closed_list = dict()
        while open_list:
            node = heappop(open_list)
            # this is necessary as there is no decrease_key available.
            if tuple(node[5]) in closed_list:
                continue
            if node[5] == self.goal_state:
                return self.buildSolution(node)
            closed_list[tuple(node[5])] = True
            for succ in self.successors(node[5]):
                if tuple(succ[1]) not in closed_list:
                    g = node[1] + 1
                    h = self.manhattan(succ[1])
                    heappush(open_list, (h, g, h, node, succ[0], succ[1]))
        return []

    # draw the state as a SVG.
    #def saveSVG(self, state, svg_file):
    #    svg = svgwrite.Drawing(filename = svg_file, size = ("300px","300px"))
    #    for i in xrange(self.N**2):
    #        y, x = 100 * (i / self.N), 100 * (i % self.N)
    #        svg.add(svg.rect(insert=(x, y),
    #                         size = ("100px", "100px"),
    #                         stroke_width = "4",
    #                         stroke = "black",
    #                         fill ="rgb(255,255,255)"))
    #        if state[i] == 0:
    #            continue
    #        svg.add(svg.text(str(state[i]), 
    #                         insert = (x + 24, y + 78), 
    #                         font_size=80))
    #    svg.save()
            
if __name__ == "__main__":
    # build a 3x3 puzzle
    puzzle = npuzzle(3)

    # hardest state (31 steps is an optimal solution)
    puzzle.init_state = [8, 6, 7, 2, 5, 4, 3, 0, 1]

    # run all algorithms
    puzzle.greedy()
    puzzle.astar()
    puzzle.breadth()
    puzzle.ucs()
    puzzle.ids()


