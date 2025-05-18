import copy
import time

class PuzzleState:
    def __init__(self, board, moves=0, previous=None):
        self.board = board
        self.moves = moves
        self.previous = previous
        self.blank_pos = self.find_blank()

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def get_neighbors(self):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        row, col = self.blank_pos

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_board = copy.deepcopy(self.board)
                new_board[row][col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[row][col]
                neighbors.append(PuzzleState(new_board, self.moves + 1, self))
        return neighbors

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

def is_goal(state):
    goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    return state.board == goal

def is_solvable(board):
    flat = [num for row in board for num in row if num != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0

def backtracking_search(initial_board, max_time=30, max_steps=100):
    if not is_solvable(initial_board):
        return None

    initial_state = PuzzleState(initial_board)
    # Kiểm tra ngay xem trạng thái ban đầu đã là mục tiêu chưa
    if is_goal(initial_state):
        return [initial_state.board]  # Trả về ngay trạng thái ban đầu, không cần di chuyển

    stack = [(initial_state, [])]  # (state, path)
    visited = set()
    visited.add(initial_state)
    start_time = time.time()

    while stack:
        if time.time() - start_time > max_time:
            return None

        current_state, path = stack.pop()
        if current_state.moves > max_steps:
            continue  # Bỏ qua nhánh nếu vượt quá số bước tối đa

        if is_goal(current_state):
            return [state.board for state in ([current_state] + path[::-1])]

        for neighbor in current_state.get_neighbors():
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, [current_state] + path))

    return None