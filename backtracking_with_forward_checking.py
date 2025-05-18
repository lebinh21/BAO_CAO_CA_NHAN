import copy

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải

def manhattan_distance(state):
    """Tính tổng khoảng cách Manhattan của mỗi ô đến vị trí mục tiêu."""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                value = state[i][j]
                for r in range(3):
                    for c in range(3):
                        if GOAL_STATE[r][c] == value:
                            distance += abs(i - r) + abs(j - c)
                            break
    return distance

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
    """Kiểm tra xem trạng thái có thể giải được không bằng số lần hoán vị."""
    flat = [num for row in state for num in row if num != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0

def forward_check(state):
    """Kiểm tra xem trạng thái có khả năng dẫn đến giải pháp không."""
    if not is_solvable(state):
        return False
    # Có thể thêm các kiểm tra khác, ví dụ: nếu heuristic quá lớn thì bỏ qua
    return True

def backtracking_with_forward_checking(initial_state, max_steps=50):
    """
    Thuật toán Backtracking với Forward Checking cho bài toán 8-puzzle.
    Trả về danh sách trạng thái (đường đi giải).
    """
    def backtrack(state, path, visited):
        # Nếu đã đạt trạng thái đích
        if state == GOAL_STATE:
            return path
        
        # Nếu vượt quá số bước tối đa
        if len(path) > max_steps:
            return None
        
        # Tạo các trạng thái láng giềng
        neighbors = generate_neighbors(state)
        # Sắp xếp các láng giềng theo heuristic để ưu tiên trạng thái tốt hơn
        neighbors.sort(key=lambda x: manhattan_distance(x))
        
        for next_state in neighbors:
            # Forward Checking: kiểm tra trạng thái có khả nghiệm không
            if tuple(map(tuple, next_state)) not in visited and forward_check(next_state):
                visited.add(tuple(map(tuple, next_state)))
                new_path = path + [next_state]
                result = backtrack(next_state, new_path, visited)
                if result is not None:
                    return result
                visited.remove(tuple(map(tuple, next_state)))
        
        return None

    # Kiểm tra trạng thái ban đầu có khả nghiệm không
    if not is_solvable(initial_state):
        print("Trạng thái ban đầu không thể giải được!")
        return []

    initial_path = [initial_state]
    visited = {tuple(map(tuple, initial_state))}
    solution = backtrack(initial_state, initial_path, visited)

    if solution:
        print("Đạt được GOAL_STATE!")
        return solution
    else:
        print("Không tìm được đường đi trong giới hạn số bước!")
        return []

def print_state(state):
    for row in state:
        print(row)
    print()

if __name__ == "__main__":
    # Trạng thái ban đầu từ hình ảnh trước đó
    initial_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
    print("Trạng thái ban đầu:")
    print_state(initial_state)
    
    solution = backtracking_with_forward_checking(initial_state, max_steps=50)
    
    if solution:
        print(f"Tổng số bước: {len(solution)}")
        for step, state in enumerate(solution):
            print(f"Bước {step}:")
            print_state(state)