import random
import copy

# Constants for the 8-puzzle
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
GRID_SIZE = 3

# GA parameters
POPULATION_SIZE = 100
MAX_GENERATIONS = 1000
MUTATION_RATE = 0.2
MAX_SEQUENCE_LENGTH = 50
MIN_SEQUENCE_LENGTH = 10

def find_blank(state):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if state[row][col] == 0:
                return row, col
    return None

def is_valid_move(blank_row, blank_col, move):
    new_row = blank_row + move[0]
    new_col = blank_col + move[1]
    return 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE

def apply_move(state, move):
    move_row, move_col = move
    blank_row, blank_col = find_blank(state)
    new_row, new_col = blank_row + move_row, blank_col + move_col

    if not is_valid_move(blank_row, blank_col, move):
        return None

    new_state = copy.deepcopy(state)
    new_state[blank_row][blank_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[blank_row][blank_col]
    return new_state

def apply_move_sequence(initial_state, sequence):
    state = copy.deepcopy(initial_state)
    path = [state]
    for move_idx in sequence:
        new_state = apply_move(state, MOVES[move_idx])
        if new_state is not None:
            state = new_state
            path.append(state)
    return state, path

def fitness(state, sequence_length):
    distance = 0
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = state[row][col]
            if value == 0:
                continue
            goal_row, goal_col = divmod(value - 1, GRID_SIZE)
            distance += abs(row - goal_row) + abs(col - goal_col)
    length_penalty = sequence_length * 0.1
    return -distance - length_penalty

def initialize_population():
    population = []
    for _ in range(POPULATION_SIZE):
        length = random.randint(MIN_SEQUENCE_LENGTH, MAX_SEQUENCE_LENGTH)
        sequence = [random.randint(0, 3) for _ in range(length)]
        population.append(sequence)
    return population

def select_parents(population, fitnesses):
    tournament_size = 5
    def tournament():
        participants = random.sample(list(zip(population, fitnesses)), tournament_size)
        return max(participants, key=lambda x: x[1])[0]

    parent1 = tournament()
    parent2 = tournament()
    while parent2 == parent1:
        parent2 = tournament()
    return parent1, parent2

def crossover(parent1, parent2):
    if not parent1 or not parent2:
        return parent1.copy() if parent1 else parent2.copy()

    point = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    for child in (child1, child2):
        if len(child) > MAX_SEQUENCE_LENGTH:
            child = child[:MAX_SEQUENCE_LENGTH]
        if len(child) < MIN_SEQUENCE_LENGTH:
            child.extend([random.randint(0, 3) for _ in range(MIN_SEQUENCE_LENGTH - len(child))])

    return child1, child2

def mutate(sequence):
    mutated = sequence.copy()
    for i in range(len(mutated)):
        if random.random() < MUTATION_RATE:
            mutated[i] = random.randint(0, 3)

    if len(mutated) < MIN_SEQUENCE_LENGTH:
        mutated.extend([random.randint(0, 3) for _ in range(MIN_SEQUENCE_LENGTH - len(mutated))])
    elif len(mutated) > MAX_SEQUENCE_LENGTH:
        mutated = mutated[:MAX_SEQUENCE_LENGTH]

    return mutated

def genetic_algorithm(initial_state):
    population = initialize_population()

    for generation in range(MAX_GENERATIONS):
        fitnesses = []
        best_path = None
        best_fitness = float('-inf')

        for sequence in population:
            final_state, path = apply_move_sequence(initial_state, sequence)
            fit = fitness(final_state, len(sequence))
            fitnesses.append(fit)

            if fit > best_fitness:
                best_fitness = fit
                best_path = path

            if final_state == GOAL_STATE:
                print(f"Solution found at generation {generation}")
                return path

        new_population = []
        best_idx = fitnesses.index(max(fitnesses))
        new_population.append(population[best_idx])

        while len(new_population) < POPULATION_SIZE:
            parent1, parent2 = select_parents(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1), mutate(child2)])

        population = new_population[:POPULATION_SIZE]

        if generation % 100 == 0:
            print(f"Generation {generation}, Best Fitness: {best_fitness}")

    return best_path

