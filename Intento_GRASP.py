import random  # Necesario para la selección aleatoria
import readTables



######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
# Estas variables incluyen información sobre los trabajadores, los puestos disponibles, y matrices que definen prioridades y niveles de experiencia (ILUO).
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)

# Entre cuantos mejores vecinos hacer random choice el GRASP
rcl_size = 3

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
    subvecinos=calcularVecinosInsert(no_fijos_activos)

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
    bestGlobalSolution = repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
    bestGlobalValue = funcionObjetivo(bestGlobalSolution)
    print("Solución inicial:", bestGlobalSolution)
    print("Puntuación de la solución inicial:", round(bestGlobalValue, 2))

    finalizado = False

    while not finalizado:
        # Generar los vecinos de la solución actual
        vecinos = generarVecinos(bestGlobalSolution)

        # Calcular la puntuación de los vecinos
        puntuaciones_vecinos = [funcionObjetivo(vecino) for vecino in vecinos]

        # Generar la Lista Restringida de Candidatos (RCL)
        rcl = grasp_generate_rcl(vecinos, puntuaciones_vecinos, rcl_size)

        # Si no hay vecinos en la RCL, se termina la búsqueda
        if not rcl:
            break

        # Seleccionar un vecino al azar de la RCL
        selected_neighbor = grasp_select_random_neighbor(rcl)

        # Evaluar la solución seleccionada
        selected_value = funcionObjetivo(selected_neighbor)

        # Actualizar la mejor solución global si la solución seleccionada es mejor
        if selected_value > bestGlobalValue:
            bestGlobalSolution = selected_neighbor
            bestGlobalValue = selected_value
        else:
            # Si no se mejora la solución global, terminar la búsqueda
            finalizado = True

    return bestGlobalSolution, round(bestGlobalValue, 2)


# Obtener los valores asignados por el equipo
equipo_usuario = "A"
array_trabajadores_disponibles = readTables.asignar_valores_por_equipo(trabajadores_por_equipo, equipo_usuario, cantidad_trabajadores, array_id_trabajadores)


# Hill Climbing devuelve la mejor solución de la distribución de trabajadores
solution, value = grasp(array_trabajadores_disponibles)
print("La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value)

