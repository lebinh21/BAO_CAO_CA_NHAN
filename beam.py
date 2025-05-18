import time
import heapq

WIDTH, HEIGHT = 600, 400
GRID_SIZE = 3
TILE_SIZE = WIDTH // 5 // GRID_SIZE
WHITE, BLACK, BLUE, RED, GREEN = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0)

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Phải, Xuống, Trái, Lên

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
        self.g = g  # Cost from start state
        self.h = manhattan_distance(state)
        self.f = self.g + self.h  # A* cost function (used for sorting)
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

def beam_search(start_state, beam_width=3):
    start_time = time.time()
    start = Puzzle(start_state)
    beam = [start]  
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    
    while beam:
        next_beam = []
        for node in beam:
            if node.is_goal():
                end_time = time.time()
                return node.get_path(), end_time - start_time
            
            for neighbor in node.get_neighbors():
                state_tuple = tuple(map(tuple, neighbor.state))
                if state_tuple not in visited:
                    visited.add(state_tuple)
                    next_beam.append(neighbor)
        
        # Sắp xếp các trạng thái theo heuristic và giữ lại beam_width trạng thái tốt nhất
        next_beam.sort(key=lambda x: x.h)  
        beam = next_beam[:beam_width]  
        
        if not beam:  
            return None, None
    
    end_time = time.time()
    return None, end_time - start_time