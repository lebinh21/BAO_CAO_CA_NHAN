import time
import sys

TILE_SIZE = 80  
GRID_SIZE = 3
WIDTH = TILE_SIZE * GRID_SIZE * 3 + 150 
HEIGHT = TILE_SIZE * GRID_SIZE + 120  

# Màu sắc
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

def heuristic(state):
    return sum(1 for i in range(GRID_SIZE) for j in range(GRID_SIZE) if state[i][j] and state[i][j] != GOAL_STATE[i][j])

def get_neighbors(state):
    neighbors = []
    x, y = next((i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if state[i][j] == 0)
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # phải, xuống, trái, lên
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def hill_climbing_8puzzle(initial_state):
    current = initial_state
    path = [current]
    while True:
        neighbors = get_neighbors(current)
        best_neighbor = min(neighbors, key=heuristic, default=None)
        if best_neighbor and heuristic(best_neighbor) < heuristic(current):
            current = best_neighbor
            path.append(current)
        else:
            return path  
