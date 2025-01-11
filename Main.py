import readTables
import itertools

######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
# Estas variables incluyen información sobre los trabajadores, los puestos disponibles, y matrices que definen prioridades y niveles de experiencia (ILUO).
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)


######### ASIGNACIÓN INICIAL #########
# Implementar una primera función que asigne trabajadores con mayor experiencia 
# (niveles 3 y 4 en la matriz ILUO) a los puestos prioritarios. 
# Los trabajadores restantes serán distribuidos usando un enfoque como el hill climbing.

def repartoTrabajadoresExperimentadosPrioridadConocimiento(prioridad, conocimiento, possibleSolution, cantidad_trabajadores, cantidad_puestos,array_trabajadores_disponibles, matriz_Prioridades, matriz_ILUO):
    """
    Asigna a los trabajadores con mayor conocimiento (ILUO 4 y 3) a los puestos principales.
    La asignación se realiza considerando las prioridades definidas en la matriz_Prioridades.
    """
    
    # Recorrer cada trabajador
    for trabajador_j in range(len(possibleSolution)):
        # print(" Id de trabajador actual = ", trabajador_j)
        
        # Verificar si el trabajador está disponible
        esteTrabajadorEstaDisponible = array_trabajadores_disponibles[trabajador_j]
        # print("el trabajador j está disponible = ", esteTrabajadorEstaDisponible )

        # Recorrer cada puesto disponible
        for puesto_i in range(cantidad_puestos):
            # print(" Id de puesto actual = ", puesto_i)

            #Verificar si este puesto no está inicialmente ocupado
            if puesto_i in possibleSolution:
                #Continuar con el siguiente puesto
                continue
            
            # Consultar la prioridad del trabajador para este puesto
            prioridadTrabajador_j_enPuesto_i = matriz_Prioridades[trabajador_j][puesto_i]
            # print("prioridadTrabajador_j_enPuesto_i = ", prioridadTrabajador_j_enPuesto_i)
            
            # Consultar el nivel de experiencia (ILUO) del trabajador en este puesto
            ILUOTrabajador_j_enPuesto_i = matriz_ILUO[trabajador_j][puesto_i]
            # print("ILUOTrabajador_j_enPuesto_i = ", ILUOTrabajador_j_enPuesto_i)
           
            # Condiciones para asignar el trabajador al puesto:
            # 1. El trabajador debe estar disponible.
            # 2. El puesto debe ser prioritario para el trabajador (prioridad = 1).
            # 3. El trabajador debe tener nivel de conocimiento ILUO de 4 o 3 para el puesto.
            # 4. El puesto no debe estar ya ocupado en la solución propuesta.
            if ( esteTrabajadorEstaDisponible == True and prioridadTrabajador_j_enPuesto_i == prioridad and (ILUOTrabajador_j_enPuesto_i == conocimiento)):
                # print("Este puesto ", puesto_i, "está vacío, se lo añado a j", trabajador_j )
                possibleSolution[trabajador_j] = puesto_i
                # print("De momento possibleSolution va así: ", possibleSolution)
    
    #Devolver la lista actualizada
    return possibleSolution

def repartoTrabajadoresExperimentados(array_trabajadores_disponibles):
    # Crear una posible solución inicial: se asignan los primeros puestos a trabajadores en orden, 
    # y los trabajadores restantes se dejan sin asignar (-1).
    possibleSolution = [-1 for i in range(cantidad_puestos)] + [-1 for i in range(cantidad_trabajadores - cantidad_puestos)]
    for prio in range(1, 10):  # Itera de 1 a 9 --> Prioridades de Prio_Maq
        for cono in range(4, 0, -1):  # Itera de 4 a 1 --> Conocimientos de ILUO
            possibleSolutionNew = repartoTrabajadoresExperimentadosPrioridadConocimiento(prio, cono, possibleSolution, cantidad_trabajadores, cantidad_puestos, array_trabajadores_disponibles, matriz_Prioridades, matriz_ILUO)
    return possibleSolutionNew


######### ASIGNACIÓN VALORES POR EQUIPO #########
def asignar_valores_por_equipo(equipo_usuario):
    return readTables.asignar_valores_por_equipo(trabajadores_por_equipo, equipo_usuario, cantidad_trabajadores, array_id_trabajadores)


######### FUNCIÓN OBJETIVO #########
def funcionObjetivo(possibleSolution):
    """
    Calcula la puntuación total de la asignación, maximizando el número de máquinas operativas y
    la asignación de trabajadores con el mayor nivel de conocimiento en puestos prioritarios.
    """
    puntuacion_total = 0

    # Recorremos cada máquina o puesto (i representa la máquina o puesto)
    for i in range(cantidad_puestos):
        
        prioridad_maquina_i = array_Maq_Prio[i]

        # Verificamos si la máquina tiene algún trabajador asignado en 'possibleSolution'
        trabajadores_en_puesto_i = []
        for index_trab in range(cantidad_trabajadores):
            # si el trabajador actual está en el puesto i, entonces nos guardamos el id del trabajador
            if i == possibleSolution[index_trab]:
                trabajadores_en_puesto_i.append(index_trab) 

        # Si hay algún trabajador asignado en los puestos de esta máquina, la consideramos operativa
        if any(trabajadores_en_puesto_i):  
            suma_prioridad_trabajadores = 0

            # Para cada trabajador (j representa el trabajadores dentro del puesto i)
            for index_trab_de_i in trabajadores_en_puesto_i:
                                
                prioridad_trabajador = matriz_Prioridades[index_trab_de_i][i]

                # Añadir a la puntuación de la máquina con el inverso de las prioridades
                suma_prioridad_trabajadores += 1 / prioridad_trabajador

            # Ponderar la puntuación de la máquina con el inverso de la prioridad de la máquina
            puntuacion_total += (1 / prioridad_maquina_i) * suma_prioridad_trabajadores

    return puntuacion_total

######### INSERT CON POSICIONES FIJAS #########
def insertVector(V, i, j):
    #inserts hacia la derecha
    if i<=j:
        lag = V[i]
        for k in (range(i, j)):
            V[k] = V[k+1]
        V[j] = lag
        return V
    #inserts hacia la izquierda
    else:
        lag = V[i]
        for k in reversed(range(j, i+1)):
            V[k] = V[k-1]
        V[j] = lag
        return V

def calcularVecinosInsert(vectorIni): 
    N = len(vectorIni)
    vecinosInsert=set()
    for i in range(0, N):
        #inserts derecha
        for j in range(i+1, N):
            vector = vectorIni.copy()
            vectLag = insertVector(vector,i,j)
            #es necesario que sea tupla para que sea hashable 
            # => para poder hacer el return con "vecino in vecinoInsert"
            vecinosInsert.add(tuple(vectLag))

        #inserts izquierda
        for j in range(0, i-1):
            vector = vectorIni.copy()
            vectLag = insertVector(vector,i,j)
            vecinosInsert.add(tuple(vectLag))

    #como los valores de la lista son los puestos de trabajo y mas de un 
    #trebajador puede estar en el mismo puesto, (o sea, los numeros de la lista
    #se pueden repetir) es necesario ir eliminando las combinaciones repetidas

    #devuelve una lista con los vecinos, sin repeticiones
    return vecinosInsert


def conseguirPuestosNoFijosActivos(lista1, lista2):
    """
    Obtiene una lista de los puestos no fijos, es decir, aquellos que no son puestos principales, y que tienen un trabajador asignado.
    """
    resultado = []
    # Crear una copia de lista1 para manejar las ocurrencias
    copia_lista1 = lista1.copy()
    
    for elemento in lista2:
        while elemento in copia_lista1:  # Mientras haya ocurrencias en copia_lista1
            resultado.append(elemento)
            copia_lista1.remove(elemento)  # Remueve una ocurrencia por vez
    
    return resultado

def generarVecinos(solucion):
    """
    Genera los vecinos de la solución.
    """

    puestos_no_fijos=[1,3,5,7,9,11,13,15]
    lista_vecinos=[]
    subvecinos=set()
    plantilla = solucion.copy()

    no_fijos_activos = conseguirPuestosNoFijosActivos(solucion,puestos_no_fijos)

    #creamos una lista con los trabajadores en los puestos fijos,
    #los puestos que podamos ir cambiando tendran valor inf
    plantilla = [float('inf') if elemento in no_fijos_activos else elemento for elemento in solucion]
    
    #generar todas las asignaciones posibles 
    subvecinos = calcularVecinosInsert(no_fijos_activos)

    for elem in subvecinos:
        elem_iter = iter(elem)
        vecino=plantilla.copy()
        for i in range(len(plantilla)):
            if plantilla[i] == float('inf'):  # Verifica si el valor es inf
                try: 
                    vecino[i] = next(elem_iter)  # Toma el siguiente elemento de elem
                except StopIteration:
                    break  
        lista_vecinos.append(vecino)
    
    return lista_vecinos


def generarVecinosNiveles(solucion):
    """
    Genera vecinos válidos considerando niveles de experiencia y prioridades.
    :param solucion: Lista que representa la asignación actual de trabajadores a puestos.
    :param matriz_ILUO: Matriz que indica los niveles de experiencia de los trabajadores en cada puesto.
    :param matriz_Prioridades: Matriz que indica las prioridades de los trabajadores para cada puesto.
    :return: Lista de soluciones vecinas válidas.
    """
    vecinos = []

    for i in range(len(solucion)):
        for j in range(len(solucion)):
            if i != j:
                # Crear una copia de la solución actual
                nuevo_vecino = solucion.copy()

                # Intercambiar trabajadores entre los puestos i y j
                nuevo_vecino[i], nuevo_vecino[j] = nuevo_vecino[j], nuevo_vecino[i]

                # Verificar validez del vecino
                if esVecinoValido(nuevo_vecino, matriz_ILUO, matriz_Prioridades):
                    vecinos.append(nuevo_vecino)

    return vecinos


def esVecinoValido(vecino, matriz_ILUO, matriz_Prioridades):
    """
    Verifica si un vecino es válido considerando restricciones de experiencia y prioridades.
    :param vecino: Solución vecina a evaluar.
    :param matriz_ILUO: Matriz que indica los niveles de experiencia de los trabajadores en cada puesto.
    :param matriz_Prioridades: Matriz que indica las prioridades de los trabajadores para cada puesto.
    :return: True si el vecino es válido, False en caso contrario.
    """
    for trabajador, puesto in enumerate(vecino):
        if puesto == -1:  # Trabajadores sin asignar siempre son válidos
            continue

        # Obtener la experiencia y prioridad del trabajador para el puesto asignado
        experiencia = matriz_ILUO[trabajador][puesto]
        prioridad = matriz_Prioridades[trabajador][puesto]

        # Condiciones de validez (puedes personalizar según tus reglas):
        # - Experiencia suficiente (por ejemplo, ILUO >= 3)
        # - Prioridad válida (por ejemplo, prioridad <= 3)
        if experiencia < 3 or prioridad > 3:
            return False

    return True


######### HILL CLIMBING #########
def greedyHillClimbing(array_trabajadores_disponibles):
    """
    Implementa el algoritmo Hill Climbing para encontrar la mejor solución de la distribución de trabajadores usando la estrategia Greedy.
    """

    #Solución inicial
    bestLocalSolution = repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
    bestGlobalSolution = bestLocalSolution
    print("Solución inicial:", bestLocalSolution)

    #Calcular la puntuación de la solución inicial
    bestLocalValue = funcionObjetivo(bestLocalSolution)
    bestGlobalValue = bestLocalValue
    print("Puntuación de la solución inicial:", round(bestLocalValue, 2))

    finalizado = False

    while not finalizado:  
        for i in bestLocalSolution:
            #Generar los vecinos de la solución actual
            vecinos = generarVecinos(bestLocalSolution)

            #Calcular la puntuación de los vecinos
            puntuaciones_vecinos = []
            for vecino in vecinos:
                puntuaciones_vecinos.append(funcionObjetivo(vecino))

            #Encontrar la mejor solución entre los vecinos
            bestLocalValue = max(puntuaciones_vecinos)
            bestLocalSolution = vecinos[puntuaciones_vecinos.index(bestLocalValue)]

            if bestLocalValue > bestGlobalValue:
                bestGlobalValue = bestLocalValue
                bestGlobalSolution = bestLocalSolution
            
            else:
                finalizado = True
                break

        
    return bestGlobalSolution, round(bestGlobalValue, 2)