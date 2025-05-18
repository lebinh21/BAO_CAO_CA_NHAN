import pygame
import time

WIDTH, HEIGHT = 600, 400
GRID_SIZE = 3
TILE_SIZE = WIDTH // 5 // GRID_SIZE
WHITE, BLACK, BLUE, RED, GREEN = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0)

# Trạng thái đích
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Phải, Xuống, Trái, Lên

class Puzzle:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
        
    def get_neighbors(self):
        neighbors = []
        x, y = self.zero_pos
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = [row[:] for row in self.state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(Puzzle(new_state, self, (nx, ny)))
        return neighbors
    
    def is_goal(self):
        return self.state == GOAL_STATE
    
    def get_path(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

def dfs(start_state):
    start = Puzzle(start_state)
    stack = [start]
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    start_time = time.time()
    
    while stack:
        node = stack.pop()
        if node.is_goal():
            end_time = time.time()
            return node.get_path(), end_time - start_time
        
        for neighbor in node.get_neighbors():
            state_tuple = tuple(map(tuple, neighbor.state))
            if state_tuple not in visited:
                visited.add(state_tuple)
                stack.append(neighbor)
    return None, None

