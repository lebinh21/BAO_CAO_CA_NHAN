import random
import copy
import numpy as np

# Constants for the 8-puzzle
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
GRID_SIZE = 3

# Q-Learning parameters
LEARNING_RATE = 0.1  # Alpha
DISCOUNT_FACTOR = 0.9  # Gamma
INITIAL_EPSILON = 0.5  # Initial epsilon for exploration
EPSILON_DECAY = 0.995  # Decay rate for epsilon
MIN_EPSILON = 0.01  # Minimum epsilon
MAX_EPISODES = 20000  # Increased training episodes
MAX_STEPS_PER_EPISODE = 200  # Increased steps per episode

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

def apply_move(state, move_idx):
    """Apply a move to the state by moving the blank tile."""
    move = MOVES[move_idx]
    blank_pos = find_blank(state)
    if blank_pos is None:
        return None
    blank_row, blank_col = blank_pos
    move_row, move_col = blank_row + move[0], blank_col + move[1]
    
    if not is_valid_move(move_row, move_col):
        return None
    
    # Swap the blank tile with the adjacent tile
    new_state = copy.deepcopy(state)
    new_state[blank_row][blank_col] = new_state[move_row][move_col]
    new_state[move_row][move_col] = 0
    return new_state

def state_to_tuple(state):
    """Convert a state (list of lists) to a tuple for hashing."""
    return tuple(tuple(row) for row in state)

def manhattan_distance(state):
    """Calculate Manhattan distance to the goal state."""
    distance = 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = state[row][col]
            if value == 0:
                goal_row, goal_col = 2, 2  # Blank tile goal position
            else:
                goal_row, goal_col = divmod(value - 1, GRID_SIZE)
            distance += abs(row - goal_row) + abs(col - goal_col)
    return distance

def get_reward(state):
    """Calculate the reward based on proximity to the goal and goal achievement."""
    distance = manhattan_distance(state)
    if state == GOAL_STATE:
        return 1000  # Large positive reward for reaching the goal
    return -distance  # Negative reward proportional to Manhattan distance

def choose_action(state, q_table, epsilon):
    """Choose an action using epsilon-greedy strategy."""
    state_key = state_to_tuple(state)
    if random.random() < epsilon:
        # Exploration: choose a random action
        return random.randint(0, 3)
    else:
        # Exploitation: choose the action with the highest Q-value
        q_values = [q_table.get((state_key, a), 0) for a in range(4)]
        return np.argmax(q_values)

def q_learning(initial_state):
    """
    Q-Learning algorithm for solving the 8-puzzle.
    Returns a list of states (solution path) that reaches the goal state.
    """
    # Initialize Q-table
    q_table = {}
    epsilon = INITIAL_EPSILON
    
    # Training phase
    for episode in range(MAX_EPISODES):
        state = copy.deepcopy(initial_state)
        for step in range(MAX_STEPS_PER_EPISODE):
            # Choose action
            action = choose_action(state, q_table, epsilon)
            
            # Take action and observe next state and reward
            next_state = apply_move(state, action)
            if next_state is None:
                # Invalid move, assign a negative reward and stay in current state
                reward = -100
                next_state = state
            else:
                reward = get_reward(next_state)
            
            # Update Q-table
            state_key = state_to_tuple(state)
            next_state_key = state_to_tuple(next_state)
            current_q = q_table.get((state_key, action), 0)
            next_q_values = [q_table.get((next_state_key, a), 0) for a in range(4)]
            max_next_q = max(next_q_values)
            
            # Q-learning update rule
            new_q = current_q + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_q - current_q)
            q_table[(state_key, action)] = new_q
            
            state = next_state
            
            # Check if goal is reached
            if state == GOAL_STATE:
                break
        
        # Decay epsilon
        epsilon = max(MIN_EPSILON, epsilon * EPSILON_DECAY)
    
    # Generate solution path using the learned Q-table
    state = copy.deepcopy(initial_state)
    path = [state]
    visited = set()
    visited.add(state_to_tuple(state))
    max_steps = 500  # Increased limit to ensure reaching the goal
    
    while state != GOAL_STATE and len(path) < max_steps:
        state_key = state_to_tuple(state)
        q_values = [q_table.get((state_key, a), 0) for a in range(4)]
        action = np.argmax(q_values)
        
        next_state = apply_move(state, action)
        if next_state is None or state_to_tuple(next_state) in visited:
            break  # Avoid invalid moves or cycles
        
        state = next_state
        visited.add(state_to_tuple(state))
        path.append(state)
        
        if state == GOAL_STATE:
            return path
    
    # If goal not reached, return the best path found
    return path
