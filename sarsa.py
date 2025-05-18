import copy
import random

GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
ACTIONS = ['up', 'down', 'left', 'right']

def state_to_tuple(state):
    """Chuyển ma trận 3x3 thành tuple để làm key trong Q-table."""
    return tuple(tuple(row) for row in state)

def find_blank(state):
    """Tìm vị trí của ô trống (0)."""
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j
    return None

def get_next_state(state, action):
    """Tạo trạng thái tiếp theo dựa trên hành động."""
    blank_x, blank_y = find_blank(state)
    dx, dy = MOVES[ACTIONS.index(action)]
    new_x, new_y = blank_x + dx, blank_y + dy
    if 0 <= new_x < 3 and 0 <= new_y < 3:
        new_state = copy.deepcopy(state)
        new_state[blank_x][blank_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[blank_x][blank_y]
        return new_state
    return None

def get_reward(state):
    """Tính phần thưởng dựa trên trạng thái."""
    if state == GOAL_STATE:
        return 100
    return -1  # Phạt nhẹ cho mỗi bước

def choose_action(state, q_table, epsilon):
    """Chọn hành động theo chính sách ε-greedy."""
    state_tuple = state_to_tuple(state)
    if random.random() < epsilon:
        return random.choice(ACTIONS)
    else:
        return max(ACTIONS, key=lambda a: q_table.get((state_tuple, a), 0.0))

def sarsa(initial_state, episodes=100, max_steps=50, alpha=0.1, gamma=0.9, epsilon=0.1):
    """Thuật toán SARSA cho bài toán 8-puzzle."""
    q_table = {}  # Bảng Q lưu giá trị Q(s, a)

    for episode in range(episodes):
        state = copy.deepcopy(initial_state)
        action = choose_action(state, q_table, epsilon)
        steps = 0
        path = [state]

        while steps < max_steps:
            next_state = get_next_state(state, action)
            if next_state is None:
                reward = -10  # Phạt nặng nếu hành động không hợp lệ
                next_action = random.choice(ACTIONS)  # Chọn ngẫu nhiên hành động tiếp theo
            else:
                reward = get_reward(next_state)
                next_action = choose_action(next_state, q_table, epsilon)
                path.append(next_state)

            state_tuple = state_to_tuple(state)
            next_state_tuple = state_to_tuple(next_state) if next_state else state_tuple
            q_table[(state_tuple, action)] = q_table.get((state_tuple, action), 0.0) + \
                alpha * (reward + gamma * q_table.get((next_state_tuple, next_action), 0.0) - q_table.get((state_tuple, action), 0.0))

            if next_state == GOAL_STATE or steps >= max_steps - 1:
                break

            state = next_state if next_state else state
            action = next_action
            steps += 1

        if next_state == GOAL_STATE:
            print(f"Episode {episode + 1}: Đạt GOAL_STATE sau {steps} bước!")
            return path
        elif episode == episodes - 1:
            print("Không đạt GOAL_STATE sau số lần học tối đa!")
            return path

def print_state(state):
    for row in state:
        print(row)
    print()

