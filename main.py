import sys
import pygame
import time
import copy
import random
import math
from A_sao import a_star
from BFS import bfs
from DFS import dfs
from greedy_search import greedy_search
from IDA_sao import ida_star
from IDS import ids
from SHC_simple import hill_climbing_8puzzle
from UCS import ucs
from Steepest_Ascent_hill_climbing import steepest_ascent_hill_climbing
from stochastic_hill_climbing import stochastic_hill_climbing
from simulated_annealing import simulated_annealing
from beam import beam_search
from and_or_search import and_or_search, Puzzle
from Belief_State_Search import belief_state_search
from bsa import backtracking_search
from sbo import belief_state_search_partically_observation
from GA import genetic_algorithm
from q_learning import q_learning
from backtracking_with_forward_checking import backtracking_with_forward_checking
from sarsa import sarsa

# Cấu hình giao diện
WIDTH, HEIGHT = 1000, 650
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RGB = (230, 230, 250)
GREEN = (40, 167, 69)
GRAY = (200, 200, 200)
RG = (255, 0, 0)
RB = (255, 105, 180)
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 40
GRID_SIZE = 3
CELL_SIZE = 70
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]
STEP_DELAY = 1.0  # Thời gian chờ giữa các bước (giây)
TILE_ANIMATION_DURATION = 0.5  # Thời gian animation cho mỗi bước (giây)

def lerp(start, end, t):
    """Linear interpolation between start and end based on t (0 to 1)"""
    return start + (end - start) * t

def draw_puzzle(screen, state, x_offset, y_offset, title="", animating=False, tile_positions=None, animation_progress=0):
    """Vẽ một bảng puzzle tại vị trí xác định, hỗ trợ animation cho ô"""
    font = pygame.font.Font(None, 28)
    title_text = font.render(title, True, BLACK)
    screen.blit(title_text, (x_offset, y_offset - 25))

    # Vẽ lưới nền
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            rect = pygame.Rect(x_offset + col * CELL_SIZE, y_offset + row * CELL_SIZE, 
                             CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

    # Vẽ các ô với vị trí có thể được animating
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = state[row][col]
            if value == 0:
                continue

            # Tính vị trí hiện tại của ô
            if animating and tile_positions and (row, col) in tile_positions:
                (start_row, start_col), (end_row, end_col) = tile_positions[(row, col)]
                current_x = lerp(x_offset + start_col * CELL_SIZE, x_offset + end_col * CELL_SIZE, animation_progress)
                current_y = lerp(y_offset + start_row * CELL_SIZE, y_offset + end_row * CELL_SIZE, animation_progress)
            else:
                current_x = x_offset + col * CELL_SIZE
                current_y = y_offset + row * CELL_SIZE

            rect = pygame.Rect(current_x, current_y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            text = font.render(str(value), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def draw_dropdown(screen, font, selected_algo, algorithms):
    """Vẽ dropdown chọn thuật toán"""
    dropdown_rect = pygame.Rect(20, 50, 200, 30)
    pygame.draw.rect(screen, WHITE, dropdown_rect)
    pygame.draw.rect(screen, BLACK, dropdown_rect, 2)
    text = font.render(selected_algo, True, BLACK)
    screen.blit(text, (dropdown_rect.x + 5, dropdown_rect.y + 5))
    return dropdown_rect

def draw_buttons(screen, font):
    """Vẽ các nút Giải và Reset"""
    solve_button = pygame.Rect(250, 30, BUTTON_WIDTH, BUTTON_HEIGHT)
    reset_button = pygame.Rect(400, 30, BUTTON_WIDTH, BUTTON_HEIGHT)
    
    pygame.draw.rect(screen, GREEN, solve_button)
    pygame.draw.rect(screen, RG, reset_button)
    
    solve_text = font.render("Giai", True, WHITE)
    reset_text = font.render("Reset", True, WHITE)
    
    screen.blit(solve_text, (solve_button.x + 20, solve_button.y + 5))
    screen.blit(reset_text, (reset_button.x + 10, reset_button.y + 5))
    
    return solve_button, reset_button

def draw_solution_steps(screen, font, solution, step_count, time_taken, scroll_y=0):
    """Hiển thị danh sách các bước giải với thanh cuộn"""
    steps_rect = pygame.Rect(500, 20, 300, 600)
    pygame.draw.rect(screen, WHITE, steps_rect)
    pygame.draw.rect(screen, BLACK, steps_rect, 2)
    
    # Tiêu đề
    title = font.render(f"Buoc hien tai: {step_count}", True, BLACK)
    screen.blit(title, (steps_rect.x + 10, steps_rect.y + 10))
    
    # Thời gian ở ngoài khung bước hiện tại
    time_text = font.render(f"Thoi gian: {time_taken:.2f}s", True, RB)
    screen.blit(time_text, (steps_rect.x - 200, steps_rect.y + 500))
    
    # Tính chiều cao nội dung và thanh cuộn
    step_height = 60
    content_height = len(solution) * step_height
    visible_height = steps_rect.height - 50
    max_scroll = max(0, content_height - visible_height)
    scroll_y = min(max(scroll_y, 0), max_scroll)
    
    # Tạo bề mặt phụ để cắt nội dung trong khung
    clip_surface = pygame.Surface((steps_rect.width, visible_height))
    clip_surface.fill(WHITE)
    
    # Vẽ thanh cuộn nếu cần
    if content_height > visible_height:
        scrollbar_rect = pygame.Rect(steps_rect.width - 20, 40, 15, visible_height)
        pygame.draw.rect(clip_surface, WHITE, scrollbar_rect)
        scroll_handle_height = (visible_height / content_height) * visible_height
        scroll_handle_y = 40 + (scroll_y / content_height) * (visible_height - scroll_handle_height)
        scroll_handle = pygame.Rect(steps_rect.width - 20, scroll_handle_y, 15, scroll_handle_height)
        pygame.draw.rect(clip_surface, WHITE, scroll_handle)
    
    # Vẽ các bước trên bề mặt phụ
    y_offset = 40 - scroll_y
    for i, state in enumerate(solution):
        step_text = font.render(f"Buoc {i+1:02d}:", True, BLACK)
        clip_surface.blit(step_text, (10, y_offset))
        state_str = str(state).replace("] [", "]\n[")
        state_text = font.render(state_str, True, BLACK)
        clip_surface.blit(state_text, (80, y_offset))
        y_offset += step_height
    
    # Vẽ bề mặt phụ lên màn hình chính
    screen.blit(clip_surface, (steps_rect.x, steps_rect.y + 40))
    
    return scroll_y

def find_tile_movements(prev_state, next_state):
    """Tìm các ô di chuyển giữa hai trạng thái"""
    tile_positions = {}
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = next_state[row][col]
            if value == 0:
                continue
            # Tìm vị trí của giá trị này trong trạng thái trước
            for prev_row in range(GRID_SIZE):
                for prev_col in range(GRID_SIZE):
                    if prev_state[prev_row][prev_col] == value:
                        if (prev_row, prev_col) != (row, col):
                            tile_positions[(row, col)] = ((prev_row, prev_col), (row, col))
                        break
    return tile_positions

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8-Puzzle Solver")
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    
    algorithms = [
        ("A*", a_star),
        ("BFS", bfs),
        ("DFS", dfs),
        ("Greedy", greedy_search),
        ("IDA*", ida_star),
        ("IDS", ids),
        ("Hill climbing", hill_climbing_8puzzle),
        ("UCS", ucs),
        ("Steepest hill", steepest_ascent_hill_climbing),
        ("Stochastic hill", stochastic_hill_climbing),
        ("SA", simulated_annealing),
        ("Beam", beam_search),  
        ("And_Or", and_or_search),  
        ("Belief state", belief_state_search),
        ("Backtracking", backtracking_search),
        ("Search Partically", belief_state_search_partically_observation),
        ("GA", genetic_algorithm),
        ("q_learning", q_learning),
        ("backtracking_forward", backtracking_with_forward_checking),
        ("sarsa", sarsa)
    ]
    selected_algo = algorithms[0][0]
    algo_dict = dict(algorithms)
    
    initial_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
    current_state = initial_state
    solution = []
    step_count = 0
    time_taken = 0.0
    current_step_index = 0
    last_step_time = 0.0
    start_time = 0.0
    scroll_y = 0
    animation_active = False
    tile_animation = False
    tile_animation_start = 0.0
    tile_positions = {}
    
    running = True
    while running:
        screen.fill(RGB)
        
        # Vẽ giao diện
        screen.blit(font.render("Chon thuat toan:", True, BLACK), (20, 20))
        dropdown_rect = draw_dropdown(screen, font, selected_algo, algorithms)
        solve_button, reset_button = draw_buttons(screen, font)
        
        draw_puzzle(screen, initial_state, 20, 120, "Trang thai ban dau:")
        # Vẽ trạng thái thực hiện với animation nếu có
        if tile_animation:
            animation_progress = min(1.0, (time.time() - tile_animation_start) / TILE_ANIMATION_DURATION)
            draw_puzzle(screen, current_state, 20, 380, "Trang thai thuc hien:", 
                       animating=True, tile_positions=tile_positions, animation_progress=animation_progress)
            if animation_progress >= 1.0:
                tile_animation = False
        else:
            draw_puzzle(screen, current_state, 20, 380, "Trang thai thuc hien:")
        draw_puzzle(screen, GOAL_STATE, 250, 120, "Trang thai dich:")
        
        if solution:
            # Tự động chuyển bước nếu đang chạy animation
            if animation_active:
                current_time = time.time()
                # Cập nhật thời gian đã trôi qua từ khi bắt đầu animation
                time_taken = current_time - start_time
                if not tile_animation and current_time - last_step_time >= STEP_DELAY:
                    if current_step_index < len(solution) - 1:
                        # Tìm các ô di chuyển để animate
                        prev_state = solution[current_step_index]
                        current_step_index += 1
                        current_state = solution[current_step_index]
                        tile_positions = find_tile_movements(prev_state, current_state)
                        tile_animation = True
                        tile_animation_start = current_time
                        last_step_time = current_time
                    else:
                        # Dừng animation khi đã hiển thị tất cả các bước trong solution
                        animation_active = False
            
            scroll_y = draw_solution_steps(screen, font, solution, step_count, time_taken, scroll_y)
        
        pygame.display.flip()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dropdown_rect.collidepoint(event.pos):
                    current_idx = [name for name, _ in algorithms].index(selected_algo)
                    selected_algo = algorithms[(current_idx + 1) % len(algorithms)][0]
                elif solve_button.collidepoint(event.pos):
                    chosen_algorithm = algo_dict[selected_algo]
                    
                    if selected_algo == "And_Or":
                        puzzle = Puzzle(initial_state)
                        result = chosen_algorithm(puzzle)
                    else:
                        result = chosen_algorithm(initial_state)
                    
                    if isinstance(result, tuple) and len(result) == 2:
                        solution, _ = result
                    else:
                        solution = result
                    
                    if solution and isinstance(solution, list):
                        step_count = len(solution) - 1
                        current_step_index = 0
                        current_state = solution[0]
                        # Bắt đầu tính thời gian khi animation chạy
                        start_time = time.time()
                        last_step_time = start_time
                        time_taken = 0.0
                        animation_active = True
                        tile_animation = False
                        tile_positions = {}
                    else:
                        solution = []
                        step_count = 0
                        current_state = initial_state
                        time_taken = 0.0
                        animation_active = False
                    scroll_y = 0
                elif reset_button.collidepoint(event.pos):
                    initial_state = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
                    current_state = initial_state
                    solution = []
                    step_count = 0
                    time_taken = 0.0
                    current_step_index = 0
                    animation_active = False
                    tile_animation = False
                    scroll_y = 0
            elif event.type == pygame.MOUSEWHEEL:
                if solution:
                    scroll_y -= event.y * 20
        
    pygame.quit()

if __name__ == "__main__":
    main()
