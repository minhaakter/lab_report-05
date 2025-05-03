import random

def create_individual(n):
    """Creates a random individual (permutation of 0 to n-1)."""
    individual = list(range(n))
    random.shuffle(individual)
    return individual

def calculate_fitness(individual):
    """Calculates number of diagonal conflicts (lower is better)."""
    n = len(individual)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(individual[i] - individual[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def selection(population, fitnesses):
    """Roulette wheel selection based on inverse fitness."""
    total_fitness = sum(1 / (1 + f) for f in fitnesses)
    probabilities = [(1 / (1 + f)) / total_fitness for f in fitnesses]
    parent1 = random.choices(population, weights=probabilities, k=1)[0]
    parent2 = random.choices(population, weights=probabilities, k=1)[0]
    return parent1, parent2

def crossover(parent1, parent2):
    """Partially Mapped Crossover (PMX-like for permutations)."""
    n = len(parent1)
    point = random.randint(1, n - 2)
    child1 = parent1[:point] + [x for x in parent2 if x not in parent1[:point]]
    child2 = parent2[:point] + [x for x in parent1 if x not in parent2[:point]]
    return child1, child2

def mutate(individual, mutation_rate):
    """Swap mutation."""
    individual = individual.copy()
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def print_board(individual):
    """Visualizes the board."""
    n = len(individual)
    print("\nChessboard:")
    for row in range(n):
        line = ""
        for col in range(n):
            if individual[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print()

def genetic_algorithm(n, population_size=100, mutation_rate=0.1, max_generations=1000):
    population = [create_individual(n) for _ in range(population_size)]

    for generation in range(max_generations):
        fitnesses = [calculate_fitness(ind) for ind in population]
        best_fitness = min(fitnesses)
        best_individual = population[fitnesses.index(best_fitness)]

        if best_fitness == 0:
            print(f"\n Solution found in generation {generation + 1}: {best_individual}")
            print_board(best_individual)
            return best_individual

        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([
                mutate(child1, mutation_rate),
                mutate(child2, mutation_rate)
            ])
        population = new_population[:population_size]

        if generation % 100 == 0:
            print(f"Generation {generation + 1} | Best Fitness: {best_fitness}")

    print("\n Maximum generations reached. Best attempt:")
    print_board(best_individual)
    return best_individual

if __name__ == "__main__":
    try:
        n_queens = int(input("Enter the number of queens (N): "))
        if n_queens > 0:
            genetic_algorithm(n_queens)
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter an integer.")
