from copy import deepcopy
from collections import deque

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
GRID_SIZE = 3
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Puzzle:
    def __init__(self, state):
        if not isinstance(state, list) or not all(isinstance(row, list) for row in state):
            raise ValueError("State must be a 2D list (e.g., [[1, 2, 3], [4, 5, 6], [7, 8, 0]])")
        self.state = state
        self.blank = self.find_blank()

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None

    def get_state_id(self):
        return tuple(tuple(row) for row in self.state)

    def is_goal(self):
        return self.state == GOAL_STATE

    def move(self, dx, dy):
        x, y = self.blank
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = deepcopy(self.state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            return Puzzle(new_state)
        return None

    def get_all_moves(self):
        next_states = []
        for dx, dy in MOVES:
            moved = self.move(dx, dy)
            if moved:
                next_states.append(moved)
        return next_states

def belief_state_search(initial_state):
   
    if not isinstance(initial_state, list) or not all(isinstance(row, list) for row in initial_state):
        raise ValueError("initial_state must be a 2D list (e.g., [[1, 2, 3], [4, 5, 6], [7, 8, 0]])")

    queue = deque([(Puzzle(initial_state), [initial_state])]) 
    visited = {tuple(tuple(row) for row in initial_state)}

    while queue:
        current_puzzle, path = queue.popleft()

        if current_puzzle.is_goal():
            return path

        for next_puzzle in current_puzzle.get_all_moves():
            state_id = next_puzzle.get_state_id()
            if state_id not in visited:
                visited.add(state_id)
                new_path = path + [next_puzzle.state]
                queue.append((next_puzzle, new_path))

    return None  