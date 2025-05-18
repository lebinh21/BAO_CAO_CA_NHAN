import time
import heapq

# Kích thước cửa sổ hiển thị
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 3
TILE_SIZE = WIDTH // 5 // GRID_SIZE
WHITE, BLACK, BLUE, RED, GREEN = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0)

def manhattan_distance(state):
    distance = 0
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = state[i][j]
            if value != 0:
                goal_x, goal_y = (value - 1) // GRID_SIZE, (value - 1) % GRID_SIZE
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance

# Trạng thái đích
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Phải, Xuống, Trái, Lên

class Puzzle:
    def __init__(self, state, parent=None, move=None, g=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g  # Cost from start state
        self.h = manhattan_distance(state)
        self.f = self.g + self.h  # A* cost function
        self.zero_pos = [(i, row.index(0)) for i, row in enumerate(state) if 0 in row][0]
    
    def __lt__(self, other):
        return self.f < other.f
    
    def get_neighbors(self):
        neighbors = []
        x, y = self.zero_pos
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                new_state = [row[:] for row in self.state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(Puzzle(new_state, self, (nx, ny), self.g + 1))
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

def ida_star(start_state):
    def search(node, threshold):
        f = node.g + node.h
        if f > threshold:
            return f, None
        if node.is_goal():
            return None, node.get_path()
        min_cost = float('inf')
        for neighbor in node.get_neighbors():
            cost, path = search(neighbor, threshold)
            if path:
                return None, path
            if cost < min_cost:
                min_cost = cost
        return min_cost, None
    
    start = Puzzle(start_state)
    threshold = start.h
    start_time = time.time()
    
    while True:
        cost, path = search(start, threshold)
        if path:
            end_time = time.time()
            return path, end_time - start_time
        if cost == float('inf'):
            return None, None
        threshold = cost
    