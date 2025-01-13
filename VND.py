import main


######### VND #########
def vnd(array_trabajadores_disponibles):
    """
    Implementa el algoritmo Variable Neighborhood Descent (VND) para encontrar la mejor solución.

    :param array_trabajadores_disponibles: Lista de trabajadores disponibles.
    :return: La mejor solución encontrada y su puntuación.
    """
    # vecindarios: Lista de funciones que generan vecinos para diferentes vecindarios.
    # Definir las funciones de vecindarios como una lista
    vecindarios = [
        main.generarVecinos,  # Vecindario 1
        main.generarVecinosNiveles,  # Vecindario 2
    ]

    # Solución inicial
    bestGlobalSolution = main.repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
    bestGlobalValue = main.funcionObjetivo(bestGlobalSolution)

    # print("Solución inicial:", bestGlobalSolution)
    # print("Puntuación de la solución inicial:", round(bestGlobalValue, 2))

    k = 0  # Índice del vecindario actual

    while k < len(vecindarios):
        # Generar los vecinos usando el vecindario k
        vecinos = vecindarios[k](bestGlobalSolution)

        # Calcular la puntuación de los vecinos
        puntuaciones_vecinos = [main.funcionObjetivo(vecino) for vecino in vecinos]

        # Encontrar el mejor vecino en este vecindario
        if vecinos:
            bestNeighborIndex = puntuaciones_vecinos.index(max(puntuaciones_vecinos))
            bestNeighbor = vecinos[bestNeighborIndex]
            bestNeighborValue = puntuaciones_vecinos[bestNeighborIndex]

            # Si el mejor vecino mejora la solución actual
            if bestNeighborValue > bestGlobalValue:
                bestGlobalSolution = bestNeighbor
                bestGlobalValue = bestNeighborValue
                # print(f"Vecindario {k}: Se encontró una mejor solución. Puntuación: {round(bestGlobalValue, 2)}")
                # Volver al primer vecindario
                k = 0
            else:
                # Pasar al siguiente vecindario
                k += 1
        else:
            # Si no hay vecinos, pasar al siguiente vecindario
            k += 1

    return bestGlobalSolution, round(bestGlobalValue, 2)