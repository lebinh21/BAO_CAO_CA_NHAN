import copy
from collections import deque

# Constants for the 8-puzzle
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
GRID_SIZE = 3

def find_blank(state):
    """Find the position of the blank tile (0)."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if state[row][col] == 0:
                return row, col
    return None

def is_valid_move(row, col):
    """Check if the position (row, col) is within the grid."""
    return 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE

def apply_move(state, move, blank_pos):
    """Apply a move to the state by moving the blank tile."""
    new_state = copy.deepcopy(state)
    blank_row, blank_col = blank_pos
    move_row, move_col = blank_row + move[0], blank_col + move[1]
    
    if not is_valid_move(move_row, move_col):
        return None
    
    # Swap the blank tile with the adjacent tile
    new_state[blank_row][blank_col] = new_state[move_row][move_col]
    new_state[move_row][move_col] = 0
    return new_state

def get_observation(state):
    """Get the observation: the position of the blank tile."""
    return find_blank(state)

def belief_state_search_partically_observation(initial_state):
    """
    Simplified Belief State Search for 8-puzzle with partial observation.
    Returns a list of states (solution path) from initial_state to goal_state.
    """
    # For simplicity, assume we know the initial state but can only observe the blank tile
    # We'll use a deterministic approach by tracking the blank tile's movement
    queue = deque([(initial_state, [initial_state])])
    visited = set()
    visited.add(tuple(map(tuple, initial_state)))
    
    while queue:
        current_state, path = queue.popleft()
        
        # Check if the current state is the goal
        if current_state == GOAL_STATE:
            return path
        
        # Get the blank tile's position (our observation)
        blank_pos = find_blank(current_state)
        
        # Try all possible moves for the blank tile
        for move in MOVES:
            new_state = apply_move(current_state, move, blank_pos)
            if new_state is None:
                continue
            
            # Convert state to tuple for hashing
            state_tuple = tuple(map(tuple, new_state))
            if state_tuple in visited:
                continue
            visited.add(state_tuple)
            
            # Add the new state to the path and queue
            new_path = path + [new_state]
            queue.append((new_state, new_path))
    
    # If no solution is found (which shouldn't happen for a solvable 8-puzzle), return None
    return None
