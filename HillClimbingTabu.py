import random  # Necesario para la selección aleatoria
import readTables
import numpy as np
from itertools import permutations
import main




######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
# Estas variables incluyen información sobre los trabajadores, los puestos disponibles, y matrices que definen prioridades y niveles de experiencia (ILUO).
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)

######### HILL CLIMBING + TABU #########
def randomHillClimbingTabu(array_trabajadores_disponibles, tabu_list_size = 10):
    """
    Implementa el algoritmo Hill Climbing para encontrar la mejor solución de la distribución de trabajadores usando la estrategia Random.
    """

    #Solución inicial
    bestLocalSolution = main.repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
    bestGlobalSolution = bestLocalSolution
    print("Solución inicial:", bestLocalSolution)

    # Inicializar TabuList
    tabuList = []
    tabuList.append(bestLocalSolution)

    #Calcular la puntuación de la solución inicial
    bestLocalValue = main.funcionObjetivo(bestLocalSolution)
    bestGlobalValue = bestLocalValue
    print("Puntuación de la solución inicial:", round(bestLocalValue, 2))

    finalizado = False

    while_i = 0
    for_i = 0
    while not finalizado: 
        while_i += 1 

        #Generar los vecinos de la solución actual DE FORMA ALEATORIA
        vecinos = main.generarVecinos(bestLocalSolution)

        #Calcular la puntuación de los vecinos
        puntuaciones_vecinos = []
        for vecino in vecinos:
            puntuaciones_vecinos.append(main.funcionObjetivo(vecino))

        #Elegir un mejor candidato
        bestLocalSolution = 0
        bestLocalValue = float('-inf')

        #Aceptar un mejor candidato siempre y cuando no esté en el tabu list
        for i in range(len(vecinos)):
            if (vecinos[i] not in tabuList) and (puntuaciones_vecinos[i] >= bestLocalValue):
                bestLocalSolution = vecinos[i] 
                bestLocalValue = puntuaciones_vecinos[i]

        tabuList.append(bestLocalSolution)
        if (len(tabuList)>tabu_list_size):
            tabuList = tabuList[1:]

        #Actualizar la mejor solución globlal
        if bestLocalValue > bestGlobalValue:
            bestGlobalValue = bestLocalValue
            bestGlobalSolution = bestLocalSolution
        else:
            finalizado = True
            print(f"Ha entrado en el while {while_i} veces")

        
    return bestGlobalSolution, round(bestGlobalValue, 2)