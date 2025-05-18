import copy

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

def steepest_ascent_hill_climbing(initial_state):
    current_state = initial_state
    current_heuristic = heuristic(current_state)
    path = [current_state]

    while current_heuristic < 8: 
        neighbors = generate_neighbors(current_state)
 
        best_state = max(neighbors, key=heuristic)
        best_heuristic = heuristic(best_state)

        if best_heuristic <= current_heuristic:
            break

        current_state = best_state
        current_heuristic = best_heuristic
        path.append(current_state)

    return path

