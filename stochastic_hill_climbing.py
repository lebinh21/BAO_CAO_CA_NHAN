import copy
import random  

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def heuristic(state):
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == GOAL_STATE[i][j]:
                count += 1
    return count  

def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

def generate_neighbors(state):
    neighbors = []
    blank_x, blank_y = find_blank(state)
    
    for dx, dy in MOVES:
        new_x, new_y = blank_x + dx, blank_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = copy.deepcopy(state)
            new_state[blank_x][blank_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[blank_x][blank_y]
            neighbors.append(new_state)
    
    return neighbors

def stochastic_hill_climbing(initial_state):
    current_state = initial_state
    current_heuristic = heuristic(current_state)
    path = [current_state]

    while True:
        neighbors = generate_neighbors(current_state)
        
        neighbor_heuristics = [(neighbor, heuristic(neighbor)) for neighbor in neighbors]
        
        if current_heuristic == 9:  
            return path, current_heuristic
     
        better_neighbors = [(state, h) for state, h in neighbor_heuristics if h > current_heuristic]

        if not better_neighbors:
            return path, current_heuristic
        
        next_state, next_heuristic = random.choice(better_neighbors)
        
        current_state = next_state
        current_heuristic = next_heuristic
        path.append(current_state)

