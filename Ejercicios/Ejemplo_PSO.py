# Particle Swarm Optimization

# ### **Problema: Minimización de una función compleja**

# Dada la función bidimensional \( f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2 \), encuentra el punto \( (x, y) \) que minimice el valor de \( f \).

# #### **Descripción de la función:**
# 1. Esta es una función conocida como *Himmelblau's Function*, que tiene múltiples mínimos locales.
# 2. Los valores de \( x \) y \( y \) deben estar dentro del rango \([-5, 5]\).

# ### **Instrucciones para el ejercicio:**

# 1. **Implementa el PSO desde cero:**
#    - Cada partícula debe tener una posición \( (x, y) \) y una velocidad \( (v_x, v_y) \).
#    - Asigna valores iniciales aleatorios para las posiciones y velocidades dentro del rango permitido.
#    - Calcula la mejor posición encontrada por cada partícula (\( p_{best} \)) y la mejor posición global (\( g_{best} \)).
#    - Ajusta las velocidades y posiciones basándote en las ecuaciones de PSO:
#      \[
#      v_{i} = w \cdot v_{i} + c_1 \cdot r_1 \cdot (p_{best} - x_{i}) + c_2 \cdot r_2 \cdot (g_{best} - x_{i})
#      \]
#      \[
#      x_{i} = x_{i} + v_{i}
#      \]
#      Donde:
#      - \( w \) es el factor de inercia.
#      - \( c_1 \) y \( c_2 \) son los coeficientes de aceleración hacia \( p_{best} \) y \( g_{best} \), respectivamente.
#      - \( r_1 \) y \( r_2 \) son valores aleatorios entre 0 y 1.

# 2. **Parámetros sugeridos:**
#    - Población de partículas: 30.
#    - Número de iteraciones: 100.
#    - \( w = 0.5 \), \( c_1 = 1.5 \), \( c_2 = 1.5 \).

# 3. **Salida esperada:**
#    - El mejor punto encontrado por el PSO (\( g_{best} \)).
#    - El valor de la función \( f(x, y) \) en ese punto.
#    - Un gráfico de convergencia mostrando el progreso del mejor valor global en cada iteración.


# CÓDIGO DE LAS TRANSPARENCIAS: 

# for each particle i = 1, ..., S do
#     Initialize the particle's position with a uniformly distributed random vector: xi ~ U(blo, bup)
#     Initialize the particle's best known position to its initial position: pi ← xi
#     if f(pi) < f(g) then
#         update the swarm's best known position: g ← pi
#     Initialize the particle's velocity: vi ~ U(-|bup-blo|, |bup-blo|)

# while a termination criterion is not met do:
#     for each particle i = 1, ..., S do
#         for each dimension d = 1, ..., n do
#             Pick random numbers: rp, rg ~ U(0,1)
#             Update the particle's velocity: vi,d ← w vi,d + φp rp (pi,d-xi,d) + φg rg (gd-xi,d)
#         Update the particle's position: xi ← xi + vi
#         if f(xi) < f(pi) then
#             Update the particle's best known position: pi ← xi
#             if f(pi) < f(g) then
#                 Update the swarm's best known position: g ← pi



import numpy as np
import matplotlib.pyplot as plt

# Parámetros globales
poblation = 30  # Número de partículas
max_iterations = 100  # Número de iteraciones
w = 0.5  # Factor de inercia
c1 = 1.5  # Coeficiente cognitivo
c2 = 1.5  # Coeficiente social
blo, bup = -5.0, 5.0  # Límites de posición
vblo, vbup = -abs(bup - blo), abs(bup - blo)  # Límites de velocidad

def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

def initialize_particles(n_particles, dimensions):
    positions = np.random.uniform(blo, bup, (n_particles, dimensions))
    velocities = np.random.uniform(vblo, vbup, (n_particles, dimensions))
    return positions, velocities

def update_velocity(velocities, positions, pbest_positions, gbest_position, w, c1, c2):
    r1, r2 = np.random.rand(*positions.shape), np.random.rand(*positions.shape)
    cognitive = c1 * r1 * (pbest_positions - positions)
    social = c2 * r2 * (gbest_position - positions)
    new_velocities = w * velocities + cognitive + social
    return np.clip(new_velocities, vblo, vbup)

def update_position(positions, velocities):
    new_positions = positions + velocities
    return np.clip(new_positions, blo, bup)

def pso():
    # Inicialización
    positions, velocities = initialize_particles(poblation, 2)
    pbest_positions = np.copy(positions)
    pbest_scores = himmelblau(positions[:, 0], positions[:, 1])
    gbest_position = pbest_positions[np.argmin(pbest_scores)]
    gbest_score = np.min(pbest_scores)

    history = []  # Para guardar los mejores valores globales por iteración
    position_history = []  # Para guardar las posiciones de todas las partículas por iteración

    for iteration in range(max_iterations):
        # Evaluación de las partículas
        scores = himmelblau(positions[:, 0], positions[:, 1])

        # Actualización de pbest
        better_mask = scores < pbest_scores
        pbest_positions[better_mask] = positions[better_mask]
        pbest_scores[better_mask] = scores[better_mask]

        # Actualización de gbest
        min_idx = np.argmin(pbest_scores)
        if pbest_scores[min_idx] < gbest_score:
            gbest_position = pbest_positions[min_idx]
            gbest_score = pbest_scores[min_idx]

        # Actualización de velocidades y posiciones
        velocities = update_velocity(velocities, positions, pbest_positions, gbest_position, w, c1, c2)
        positions = update_position(positions, velocities)

        # Registro de la historia
        history.append(gbest_score)
        position_history.append(np.copy(positions))

    return gbest_position, gbest_score, history, position_history

def plot_convergence(history):
    plt.figure(figsize=(8, 6))
    plt.plot(history, marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Best Score')
    plt.title('Convergence of PSO')
    plt.grid()
    plt.show()

def plot_positions(position_history):
    position_history = np.array(position_history)
    iterations = position_history.shape[0]
    particles = position_history.shape[1]

    plt.figure(figsize=(10, 8))
    for i in range(particles):
        plt.plot(
            range(iterations),
            position_history[:, i, 0],
            label=f'Particle {i+1} (x)',
            alpha=0.7
        )
        plt.plot(
            range(iterations),
            position_history[:, i, 1],
            label=f'Particle {i+1} (y)',
            linestyle='dashed',
            alpha=0.7
        )

    plt.xlabel('Iteration')
    plt.ylabel('Position')
    plt.title('Evolution of Particle Positions')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid()
    plt.tight_layout()
    plt.show()

def show_particles_all_iterations(particles_data_list, title):
    # Create the figure for the final plot
    plt.figure(figsize=(8, 6))

    # Define a colormap
    cmap = plt.cm.viridis
    num_iterations = len(particles_data_list)

    # Loop through each iteration's data and plot
    for iter, data in enumerate(particles_data_list):
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]

        # Plot each iteration with a different color
        plt.scatter(x_values, y_values, color=cmap(iter / num_iterations), label=f'Iteration {iter}')

    # Set axis limits
    plt.xlim([-6, 6])
    plt.ylim([-6, 6])

    # Add labels and title
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # Show the final plot
    plt.show()

def main():
    gbest_position, gbest_score, history, position_history = pso()
    print(f"Best position: {gbest_position}")
    print(f"Best score: {gbest_score}")
    plot_convergence(history)
    plot_positions(position_history)
    show_particles_all_iterations(position_history, "Particle Positions Through Iterations")

if __name__ == "__main__":
    main()
