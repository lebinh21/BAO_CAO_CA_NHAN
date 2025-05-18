import time
from copy import deepcopy

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
GRID_SIZE = 3

def manhattan_distance(state):
    distance = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = (value - 1) // GRID_SIZE, (value - 1) % GRID_SIZE
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

class Puzzle:
    def __init__(self, state, parent=None, move=None, g=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g
        self.h = manhattan_distance(state)
        self.zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]

    def get_state_id(self):
        return tuple(tuple(row) for row in self.state)

    def is_goal(self):
        return self.state == GOAL_STATE

    def get_possible_moves(self):
        neighbors = []
        x, y = self.zero_pos
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = [row[:] for row in self.state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(Puzzle(new_state, self, (nx, ny), self.g + 1))
        return neighbors

def and_or_search(puzzle, visited=None, depth=0, max_depth=30):
    if visited is None:
        visited = set()

    state_id = puzzle.get_state_id()

    if puzzle.is_goal():
        path = []
        current = puzzle
        while current:
            path.append(current.state)
            current = current.parent
        return path[::-1] 

    if state_id in visited or depth > max_depth:
        return None  

    visited.add(state_id)

    for neighbor in puzzle.get_possible_moves():
        outcomes = [neighbor]

        for outcome in outcomes:
            subpath = and_or_search(outcome, visited.copy(), depth + 1, max_depth)
            if subpath is not None: 
                return subpath

    return None  