import matplotlib.pyplot as plt # Import the math plot for the graph
import math  # Import the math module
import random # Para crossover y mutación

# Ejercicio propuesto - MÍNIMO: 
# Implementa el NSGA-II o el SPEA - II, pero si haces NSGA-2 no hagas crowd distance.
# Se pide que el archivo final sea la última diapostiva del tema 5

# 1. Two objectives to optimize.

# 2. Constrained optimization problem
# Feasible vs. unfeasible.

# 3. Assign inf value to infeasible / no factibles solutions.

# 4. Implementa un algoritmo genético que podrás reutilizar en tu proyecto. Escoge el operador de cruce y mutación que te parezca más adecuado, pero cíñete a la selección basada en la frontera pareto del NSGA-II.

# 5. Entrega una imagen en la que se vea el espacio de búsqueda y la frontera pareto a lo largo de unas iteraciones

#EXTRA : implementa el PSO, enseña como las párticulas de PSO convergen en los puntos que nos interesan
# Pero PSO no es multibojetivo, siempre guardabamos EL MEJOR, ahora no hay mejor, hay una frontera psareto. 

##### AYUDANTES

def dominates (solution_a, solution_b):
    """
    check if solution_a dominates solution_b.
    """
    is_at_least_as_good_in_all_objectives = True
    is_better_in_at_least_one_objective = False

    for i in range(len(solution_a)):
        if solution_a[i] < solution_b[i]:
            is_at_least_as_good_in_all_objectives = False
            break
        if solution_a[i] > solution_b[i]:
            is_better_in_at_least_one_objective = True

    return is_at_least_as_good_in_all_objectives and is_better_in_at_least_one_objective

def find_pareto_frontier (solutions):
    """
    Find the Pareto frontier fróm a set of solutions.
    """
    pareto_frontier = []

    for i, solution_a in enumerate (solutions): 
        is_dominated = False

        for j, solution_b in enumerate (solutions):

            if i != j and dominates (solution_b, solution_a): 
                is_dominated = True 
                break

        if not is_dominated: 
            pareto_frontier.append(solution_a)

    return pareto_frontier

def show_pareto_frontier(pareto_frontier, title):
    # Extract x and y values
    x_values = [point[0] for point in pareto_frontier]
    y_values = [point[1] for point in pareto_frontier]

    # Create the scatterplot
    plt.figure(figsize=(8, 6))  # Optional: Set the figure size
    plt.scatter(x_values, y_values, color='blue', label='Pareto Frontier')

    # Add labels and title
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.title(title)
    plt.legend()

    # Show grid for better readability (optional)
    plt.grid(True)

    # Display the scatterplot
    plt.show()


def show_pareto_frontier_all_generations(generations_data):
    # Create the figure for the final plot
    plt.figure(figsize=(8, 6))

    # Define a colormap
    cmap = plt.cm.viridis
    num_generations = len(generations_data)
    
    # Loop through each generation's data and plot
    for gen, data in enumerate(generations_data):
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]
        
        # Plot each generation with a different color
        plt.scatter(x_values, y_values, color=cmap(gen / num_generations), label=f'Generation {gen}')

    # Add labels and title
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.title('Pareto Fronts Evolution Across Generations')
    plt.legend()
    plt.grid(True)
    
    # Show the final plot
    plt.show()

# Constraint 1
def C1(x1, x2):
    value = x1**2 + x2**2 - 1 - 0.1 * math.cos(16 * math.atan(x1 / x2))
    return value >= 0

# Constraint 2
def C2(x1, x2):
    value = (x1 - 0.5)**2 + (x2 - 0.5)**2
    return value <= 0.5

# Range of possible values / Search domain
def possible_values(x1, x2):
    value1 = 0 <= x1 <= math.pi  # Check if x1 is in range [0, π]
    value2 = 0 <= x2 <= math.pi  # Check if x2 is in range [0, π]
    return value1 and value2

def min_f1(x1,x2): return x1
def min_f2(x1,x2): return x2

def evaluate_solution(x1, x2):
    # Check if solution is feasible
    if not (C1(x1, x2) and C2(x1, x2)):
        return [float('inf'), float('inf')]  # Penalize infeasible / no factibles solutions
    return [min_f1(x1, x2), min_f2(x1, x2)]

# Función para calcular la distancia euclidiana entre dos soluciones
def euclidean_distance(sol1, sol2):
    return math.sqrt((sol1[0] - sol2[0])**2 + (sol1[1] - sol2[1])**2)

# Función para calcular el centroide de un conjunto de soluciones
def calculate_centroid(front):
    num_solutions = len(front)
    centroid = [sum([sol[i] for sol in front]) / num_solutions for i in range(len(front[0]))]
    return centroid

def crossover(parent1, parent2):
    # Blend crossover: average of parents
    return [
        (parent1[0] + parent2[0]) / 2,
        (parent1[1] + parent2[1]) / 2
    ]

def mutate(solution, mutation_rate=0.1):
    # Small random perturbation
    return [
        solution[0] + mutation_rate * (random.random() - 0.5),
        solution[1] + mutation_rate * (random.random() - 0.5)
    ]

# NSGA-II principal
# 1. Inicialización: Se crea una población aleatoria de soluciones.
# 2. Evaluación: Se calcula la aptitud (fitness) de cada solución.
# 3. Clasificación: Se forman los frentes de Pareto.
# 4. Selección: Se seleccionan soluciones del frente de Pareto según su distancia de hacinamiento (crowding distance).
# 5. Cruce y mutación: Se generan nuevas soluciones (descendencia).
# 6. Reemplazo: Combina las soluciones actuales con las nuevas para la siguiente generación.
# 7. Visualización: Muestra los frentes en intervalos definidos.

# NSGA-II principal
def NSGA2(population_size, num_generations):

    generations_data = []  # Store data for each generation to plot later

    # Inicializar una población aleatoria
    population = [
        [random.uniform(0, math.pi), random.uniform(0, math.pi)]
        for _ in range(population_size)
    ]
    print("STEP 1: POPULATION = ", population)

    for generation in range(num_generations):
        print(" ---------------- iteración de generación = ", generation, "----------------")

        # Evaluar la población
        evaluated_population = [
            ind + evaluate_solution(ind[0], ind[1])
            for ind in population
        ]
        print("STEP 2: EVALUATED POPULATION = ", evaluated_population)

        # Clasificar en frentes de Pareto
        pareto_front = find_pareto_frontier(evaluated_population)
        print("STEP 3: PARETO FRONT = ", pareto_front)

        # Selección usando Distancia Euclidiana
        # Calcular el centroide del frente
        centroid = calculate_centroid(pareto_front)
        
        # Ordenar soluciones por distancia euclidiana al centroide
        sorted_front = sorted(pareto_front, key=lambda sol: euclidean_distance(sol, centroid))
        print("STEP 4: SELECTED SOLUTIONS (sorted by Euclidean Distance) = ", sorted_front)

        # Extraer soluciones seleccionadas del frente de Pareto
        population = [ind[:2] for ind in sorted_front]
        print("STEP 4: NEW POPULATION = ", population)

        # Descendencia (Cruce y Mutación)
        offspring = []
        while len(offspring) < population_size:
            p1, p2 = random.sample(population, 2)
            child = mutate(crossover(p1, p2))
            offspring.append(child)
        print("STEP 5: OFFSPRING = ", offspring)

        # Combinar descendencia con el frente de Pareto para la siguiente generación
        population = population + offspring
        population = population[:population_size]
        print("STEP 6: POPULATION = ", population)

        # Visualizar la población
        # if generation % 10 == 0 or generation == num_generations - 1:
        #     show_pareto_frontier([[ind[0], ind[1]] for ind in population])
        # show_pareto_frontier([[ind[0], ind[1]] for ind in population], "Pareto Frontier Scatterplot iteration " + str(generation))

        # Store the Pareto front of this generation for plotting later
        if generation % 10 == 0 or generation == num_generations - 1:
            generations_data.append([[ind[0], ind[1]] for ind in population])

    # Visualizar los frentes de Pareto de todas las generaciones
    show_pareto_frontier_all_generations(generations_data)

    # Devolver el último frente de Pareto
    return find_pareto_frontier(evaluated_population)


# # Test find_parteo_frontier
# solutions = [
#     [3,5],
#     [4,4],
#     [5,3],
#     [2,6],
#     [6,2],
# ]
# pareto_frontier = find_pareto_frontier(solutions)
# print("Pareto Frontier:", pareto_frontier)
# show_pareto_frontier(pareto_frontier)

# Test NSGA2
population_size = 10
num_generations = 100
pareto_frontier = NSGA2(population_size, num_generations)


