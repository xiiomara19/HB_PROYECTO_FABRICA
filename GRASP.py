import random  # Necesario para la selección aleatoria
import readTables
import main

## Greedy randomized adaptive search procedure = GRASP

######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
# Estas variables incluyen información sobre los trabajadores, los puestos disponibles, y matrices que definen prioridades y niveles de experiencia (ILUO).
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)


######### RCL #########

def grasp_generate_rcl(vecinos, puntuaciones_vecinos, rcl_size=3):
    """
    Genera una Lista Restringida de Candidatos (RCL) con los mejores vecinos.
    Si hay menos de `rcl_size` vecinos, se incluyen todos.
    """
    # Combinar vecinos y puntuaciones en una lista de tuplas, y ordenar por puntuación descendente
    vecinos_puntuados = list(zip(vecinos, puntuaciones_vecinos))
    vecinos_puntuados.sort(key=lambda x: x[1], reverse=True)  # Orden descendente por puntuación

    # Seleccionar los mejores rcl_size vecinos
    rcl = vecinos_puntuados[:rcl_size]

    # Retornar solo los vecinos (sin las puntuaciones)
    return [vecino[0] for vecino in rcl]

def grasp_select_random_neighbor(rcl):
    """
    Selecciona un vecino al azar de la RCL.
    """
    return random.choice(rcl)


######### GRASP #########
def grasp(array_trabajadores_disponibles, rcl_size=3):
    """
    Implementa el algoritmo GRASP para encontrar la mejor solución de la distribución de trabajadores.
    """

    # Solución inicial
    bestGlobalSolution = main.repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
    bestGlobalValue = main.funcionObjetivo(bestGlobalSolution)
    print("Solución inicial:", bestGlobalSolution)
    print("Puntuación de la solución inicial:", round(bestGlobalValue, 2))

    finalizado = False

    while_i = 0
    while not finalizado:
        while_i += 1 
        # Generar los vecinos de la solución actual
        vecinos = main.generarVecinos(bestGlobalSolution)

        # Calcular la puntuación de los vecinos
        puntuaciones_vecinos = [main.funcionObjetivo(vecino) for vecino in vecinos]

        # Generar la Lista Restringida de Candidatos (RCL)
        rcl = grasp_generate_rcl(vecinos, puntuaciones_vecinos, rcl_size)

        # Si no hay vecinos en la RCL, se termina la búsqueda
        if not rcl:
            break

        # Seleccionar un vecino al azar de la RCL
        selected_neighbor = grasp_select_random_neighbor(rcl)

        # Evaluar la solución seleccionada
        selected_value = main.funcionObjetivo(selected_neighbor)

        # Actualizar la mejor solución global si la solución seleccionada es mejor
        if selected_value > bestGlobalValue:
            bestGlobalSolution = selected_neighbor
            bestGlobalValue = selected_value
        else:
            # Si no se mejora la solución global, terminar la búsqueda
            finalizado = True
            print(f"Ha entrado en el while {while_i} veces")

    return bestGlobalSolution, round(bestGlobalValue, 2)


