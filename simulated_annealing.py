import copy
import random
import math

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def manhattan_distance(state, goal):
    """Tính tổng khoảng cách Manhattan của mỗi ô đến vị trí mục tiêu."""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                value = state[i][j]
                for r in range(3):
                    for c in range(3):
                        if goal[r][c] == value:
                            distance += abs(i - r) + abs(j - c)
                            break
    return distance

def linear_conflict(state, goal):
    """Tính số xung đột tuyến tính để cải thiện heuristic."""
    conflict = 0
    # Kiểm tra hàng
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                val = state[i][j]
                for k in range(j + 1, 3):
                    if state[i][k] != 0 and state[i][k] != goal[i][k]:
                        goal_pos_val = [(r, c) for r in range(3) for c in range(3) if goal[r][c] == val][0]
                        goal_pos_k = [(r, c) for r in range(3) for c in range(3) if goal[r][c] == state[i][k]][0]
                        if goal_pos_val[0] == goal_pos_k[0] and goal_pos_val[1] > goal_pos_k[1]:
                            conflict += 2
    # Kiểm tra cột (tương tự)
    for j in range(3):
        for i in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                val = state[i][j]
                for k in range(i + 1, 3):
                    if state[k][j] != 0 and state[k][j] != goal[k][j]:
                        goal_pos_val = [(r, c) for r in range(3) for c in range(3) if goal[r][c] == val][0]
                        goal_pos_k = [(r, c) for r in range(3) for c in range(3) if goal[r][c] == state[k][j]][0]
                        if goal_pos_val[1] == goal_pos_k[1] and goal_pos_val[0] > goal_pos_k[0]:
                            conflict += 2
    return conflict

def heuristic(state):
    """Kết hợp Manhattan Distance và Linear Conflict."""
    return manhattan_distance(state, GOAL_STATE) + linear_conflict(state, GOAL_STATE)

def find_blank(state):
    """Tìm vị trí của ô trống (0)."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

def generate_neighbors(state):
    """Tạo tất cả các trạng thái láng giềng bằng cách di chuyển ô trống."""
    neighbors = []
    blank_x, blank_y = find_blank(state)
    
    for dx, dy in MOVES:
        new_x, new_y = blank_x + dx, blank_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = copy.deepcopy(state)
            new_state[blank_x][blank_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[blank_x][blank_y]
            neighbors.append(new_state)
    
    return neighbors

def is_solvable(state):
    """Kiểm tra xem trạng thái có thể giải được không."""
    flat = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0

def simulated_annealing(initial_state, max_steps=50):
    """
    Simulated Annealing cho bài toán 8-puzzle với giới hạn số bước.
    Trả về danh sách trạng thái (đường đi giải).
    """
    if not is_solvable(initial_state):
        print("Trạng thái ban đầu không thể giải được!")
        return []

    current_state = copy.deepcopy(initial_state)
    current_heuristic = heuristic(current_state)
    path = [current_state]
    
    temperature = 3000.0  # Tăng nhiệt độ ban đầu
    cooling_rate = 0.995  # Giảm tốc độ làm nguội
    max_iterations = 6000  # Tăng số lần lặp
    
    iteration = 0
    while iteration < max_iterations and len(path) < max_steps:
        if current_state == GOAL_STATE:
            print("Đạt được GOAL_STATE!")
            break
        
        neighbors = generate_neighbors(current_state)
        next_state = random.choice(neighbors)
        next_heuristic = heuristic(next_state)

        delta = next_heuristic - current_heuristic

        if delta < 0 or random.random() < math.exp(-delta / max(temperature, 0.0001)):
            current_state = next_state
            current_heuristic = next_heuristic
            path.append(current_state)
            if current_state == GOAL_STATE:
                print("Đạt được GOAL_STATE!")
                break

        temperature *= cooling_rate
        iteration += 1

        if iteration % 1000 == 0:
            print(f"Iteration {iteration}, Heuristic: {current_heuristic}, Temperature: {temperature:.2f}")
    
    if current_state != GOAL_STATE:
        print("Không đạt được GOAL_STATE trong giới hạn số bước hoặc số lần lặp.")
    return path

def print_state(state):
    for row in state:
        print(row)
    print()
