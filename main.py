import table
import random

######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

#Crear instancia de la clase Table
dataTable = table.Table(archivo)

def asignarTL(grupo, trabajadores, sol):
    for ind in range(dataTable.cantidad_trabajadores):
        print(ind)
        if trabajadores[ind] and dataTable.matriz_Prioridades[ind][10]==1 and dataTable.array_id_trabajadores[ind] in dataTable.trabajadores_por_equipo[grupo]:
            sol[ind]=10
            print("TL = ", ind)
            return True
    
    print("ERROR: no hay team leader para el turno")
    return False

def trabajadoresPosibles(lista_puestos_ppal, trabajadores, grupo):
    puestos_y_trabajadores=[[p] for p in lista_puestos_ppal]
    for ind in range(len(lista_puestos_ppal)):
        trabajadoresPosibles = []
        puesto = lista_puestos_ppal[ind]
        for i_tr in range(dataTable.cantidad_trabajadores):
            #si el trabajador está disponible
            if trabajadores[i_tr]==True :
                #si el trabajador tiene experiencia suficiente en el puesto
                if dataTable.matriz_ILUO[i_tr][puesto] >= 3:
                    prio_tr_en_maq = dataTable.matriz_Prioridades[i_tr][puesto]
                    pertenece_a_grupo = dataTable.array_id_trabajadores[i_tr] in dataTable.trabajadores_por_equipo[grupo]
                    #añadimos a trabajadoresPosibles el trabajador, su prioridad en el puesto y si pertenece al grupo
                    trabajadoresPosibles.append([i_tr, prio_tr_en_maq, pertenece_a_grupo])

        #primera posicion de cada sublista: puesto de trabajo
        #segunda posicion de cada sublista: lista de los datos del trabajador 
        puestos_y_trabajadores[ind].append(trabajadoresPosibles)
    #devuelve los trabajadores en el orden en el que salen en la matriz del excel, por eso luego hay que ordenarlos por prioridad
    return puestos_y_trabajadores

def eliminarTrabajadorDeSublistas(lista, id_trabajador):
   # print("lista antes de eliminar tranabajador: ", id_trabajador, " : ", lista)
    for sublista in lista:    
        sublista[1:] = [tr for tr in sublista[1:] if tr[0] != id_trabajador]
   # print("lista despues de eliminar tranabajador: ", lista)


######### ASIGNACIÓN INICIAL #########
# Implementar una primera función que asigne trabajadores con mayor experiencia 
# (niveles 3 y 4 en la matriz ILUO) a los puestos prioritarios. 
# Los trabajadores restantes serán distribuidos usando un enfoque como el hill climbing.


def asignacionIni(grupo, trabajadores):
    puestos_ppal=[0,2,4,6,8,12,14]
    refuerzos=[]
    sol1 = [-1 for i in range(dataTable.cantidad_trabajadores)]

    if not asignarTL(grupo, trabajadores, sol1):
        return False
    #asignamos los puestos principales
    asignacionIniPuestosPpal(grupo, trabajadores, sol1)
    #asignamos los puestos secundarios
    asignacionIniPuestosSec(trabajadores, sol1)

    #los trabajadores que no se hayan podido asignar a ningun puesto secundario iran como refuerzos
    for ind in range(dataTable.cantidad_trabajadores):
        if trabajadores[ind] and sol1[ind]==-1:
            refuerzos.append(ind)

    #despues de asignar los puestos principales y secundarios,
    #comprobamos si para todos los puestos principales, su puesto de ayudante está asignado
    #si el puesto de ayudante no está asignado, es decir, no hay trabajadores que puedan ocupar ese puesto,
    #tenemos que desasignar el puesto principal

    for puesto in puestos_ppal:
        if puesto not in sol1:
            for i in range(len(sol1)):
                if sol1[i]==puesto:
                    sol1[i]=-1
                    refuerzos.append(i)
    #como ahora ese trabajador está sin asignar, vamos a meterle de refuerzo en un puesto secundario
    asignacionRefuerzos(refuerzos, sol1)

   # print("=====================================")
   # print("solucion inicial: ", sol1)
    return sol1

def asignacionRefuerzos(trabajadores, sol):
    #los puestos secundaios que se pueden reforzar son:
    # 11(solo puede haber una persona de refuerzo)*, 13 o 15
    #vamos a asignar al trabajador en el primer puesto secundario de prioridad prio 
    puetos_a_reforzar = [11,13,15]
    for prio in range(1,10):
        for tr in trabajadores:
            for puesto in puetos_a_reforzar:
                    if dataTable.array_id_trabajadores[puesto]==prio: 
                        if puesto == 11 and sol.count(11)<2 and dataTable.matriz_ILUO[tr][11]>0:
                            sol[tr]=11
                        elif puesto != 11 and dataTable.matriz_ILUO[tr][puesto]>0:
                            sol[tr]=puesto

    #* el puesto 11 es distinto a los demas porque no tiene un puesto principal y otro de ayudante con indices distintos
    #ambos son el numero 11, por eso, como maximo puede haber dos personas en ese puesto


def asignacionIniPuestosPpal(grupo, trabajadores, sol):
    puestos_principales = [0,2,4,6,8,11,12,14] #el puesto de TL no se tiene en cuenta porque es un caso especial
    posibles_candidatos = []
    
    for prio in range(1,10):
      #  print("__________________________________")
       # print("prioridad: ", prio)

        parada = False
        #lista de los puestos principales con prioridad "prio"
        lista_puestos_ppal = [puesto for puesto in range(len(dataTable.array_Maq_Prio)) if dataTable.array_Maq_Prio[puesto]==prio and puesto in puestos_principales]
        if not lista_puestos_ppal:
            break
        posibles_candidatos=[[p] for p in lista_puestos_ppal]
        puestos_que_se_pueden_completar=[]

        #puestos_y_trabajadores es una lista de listas, donde cada sublista tiene el puesto y los trabajadores posibles para ese puesto
        puestos_y_trabajadores = trabajadoresPosibles(lista_puestos_ppal, trabajadores, grupo)
      #  print("puestos y trabajadores: ", puestos_y_trabajadores)

        for ind, puesto in enumerate(lista_puestos_ppal):   
            #el bucle ordena los posibles trabajadores por prioridad
            for pri in range(1,4):
             #   print("prioridad del 1 al 3: ", pri)
                #primero metemos en posibles_candidatos el indice del trabajador con prioridad "pri" y que pertenecen al grupo 
                candidato=[sub for sub in puestos_y_trabajadores[ind][1] if sub[1]==pri and sub[2]==True]
                #para evitar añadir listas vacias
                if candidato:
                    posibles_candidatos[ind].extend(candidato)
                #luego, metemos a un trabajador con prioridad pri aunque no pertenezca al grupo 
                candidato=[sub for sub in puestos_y_trabajadores[ind][1] if sub[1]==pri and sub[2]==False]
                if candidato:
                    posibles_candidatos[ind].extend(candidato)
              #  print("puestos y sus podibles candidatos ordenados: ", posibles_candidatos)
            #si hay alguien que pueda cubrir el puesto, lo añadimos a puestos_que_se_pueden_completar
            if len(posibles_candidatos[ind])>1:
                puestos_que_se_pueden_completar.append(puesto)
      #  print("puestos que se pueden completar: ", puestos_que_se_pueden_completar)
       # print("puestos y sus podibles candidatos ordenados: ", posibles_candidatos)
        #vamos a generar una primera solucion para el best first
     #   print("===========ASIGNACION DE PUESTOS================")
        while not parada:
            for ind, puesto in enumerate(puestos_que_se_pueden_completar):
                #si existe al menos un trabajador que pueda ocupar el puesto (posibles_candidatos[ind] va a tener siempre al menos un elemento -> el numero del puesto)
                if len(posibles_candidatos[ind])>1:
                    #hay que tener en cuenta que en la primera posicion de cada sublista está el puesto, 
                    #por lo que hay que contar los elementos a partir del segundo ([1:])
                    #si solo hay un trabajador que pueda ocupar el puesto, lo asignamos directamente
                    if len(posibles_candidatos[ind][1:])==1 and puesto not in sol:
                        id_trabajador = posibles_candidatos[ind][1][0]
                        if sol[id_trabajador]==-1:
                            sol[id_trabajador]=puesto
                            #trabajadores_asignados.append(id_trabajador)
                        #y lo eliminamos de los los demás puestos en los que podría estar
                        eliminarTrabajadorDeSublistas(posibles_candidatos, id_trabajador)
                        #eliminamos el trabajador si lo acabamos de asignar o si ya ha sido asignado antes,
                        #por eso estáfuera del if
                   #     print("solucion parcial: ", sol)

            for ind, puesto in enumerate(puestos_que_se_pueden_completar):   
                if len(posibles_candidatos[ind])>1:    
                    #si hay más de uno elegimos el primero
                    if len(posibles_candidatos[ind][1:])>1 and puesto not in sol:
                        id_trabajador = posibles_candidatos[ind][1][0]
                        if sol[id_trabajador]==-1:    
                            sol[id_trabajador]=puesto
                        #trabajadores_asignados.append(id_trabajador)
                        eliminarTrabajadorDeSublistas(posibles_candidatos, id_trabajador)
                   #     print("solucion parcial: ", sol)

                #es necesario dividirlo en dos 'if' por si se da un caso igual a este:
                # en el puesto 0 pueden estar los trabajadores 4 y 5 y en el puesto 2 solo puede estar el trabajador 4
                # lo más optimo sería que el trabajador 4 estuviera en el puesto 2 y el trabajador 5 en el puesto 0
                #hay que dividirlo en dos bucles para que primero asigne todos los puestos a los que solo puede ir un trabajador
       #     print("solucion parcial: ", sol)
       #     print("")
        #    print("posibles: ", posibles_candidatos)
         #   print("")
            #primer parentesis all: si todos los puesto que se podian completar aparecen en la solucion => parar
            #segundo parentesis all: si no queda ningun trabajador que pueda ocupar un puesto => parar
            parada = all(elem in sol for elem in puestos_que_se_pueden_completar) or all(len(posibles_candidatos[i])==1 for i in range(len(posibles_candidatos)))

   # sol = bestFirst(puestos_y_trabajadores_ordenados, grupo, sol)
    print("solucion", sol)
    return sol

def asignacionIniPuestosSec(trabajadores, sol):
    puestos_sec=[1,3,5,7,9,13,15]

    for tr in range(dataTable.cantidad_trabajadores):
        if trabajadores[tr] and sol[tr]==-1:
            for puesto in puestos_sec:
                #si el trabajador puede ocupar ese puesto (ILUO>0),
                #el puesto principal de la maquina esta ocupado,
                #el trabajador no esta ya en un puesto
                #y el puesto secundario esta sin asignar
                if dataTable.matriz_ILUO[tr][puesto]>0 and puesto-1 in sol and puesto not in sol:
                    #asignamos el puesto secundario
                    sol[tr]=puesto
                    break
    print("solucion con asignacion de puestos secundarios: ", sol)



    
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
        for puesto_i in range(dataTable.cantidad_puestos):
            # print(" Id de puesto actual = ", puesto_i)

            #Verificar si este puesto no está inicialmente ocupado
            if puesto_i in possibleSolution:
                #Continuar con el siguiente puesto
                continue
            
            # Consultar la prioridad del trabajador para este puesto
            prioridadTrabajador_j_enPuesto_i = dataTable.matriz_Prioridades[trabajador_j][puesto_i]
            # print("prioridadTrabajador_j_enPuesto_i = ", prioridadTrabajador_j_enPuesto_i)
            
            # Consultar el nivel de experiencia (ILUO) del trabajador en este puesto
            ILUOTrabajador_j_enPuesto_i = dataTable.matriz_ILUO[trabajador_j][puesto_i]
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
    possibleSolution = [-1 for i in range(dataTable.cantidad_puestos)] + [-1 for i in range(dataTable.cantidad_trabajadores - dataTable.cantidad_puestos)]
    for prio in range(1, 10):  # Itera de 1 a 9 --> Prioridades de Prio_Maq
        for cono in range(4, 0, -1):  # Itera de 4 a 1 --> Conocimientos de ILUO
            possibleSolutionNew = repartoTrabajadoresExperimentadosPrioridadConocimiento(prio, cono, possibleSolution, array_trabajadores_disponibles)
    return possibleSolutionNew


######### ASIGNACIÓN VALORES POR EQUIPO #########
def asignar_valores_por_equipo(equipo_usuario):
    valida = False
    while not valida:
        respuesta = input("¿Hay alguna falta en el equipo? (si/no) ").strip()
        if respuesta.lower() == "si":
            faltas = input("Escribe el identificador de los trabajadores que no han asistido separados por comas: ")
            faltas = [int(falta.strip()) for falta in faltas.split(",")]
            valida = True
        
        elif respuesta.lower() == "no" :
            faltas = []
            valida = True
        
        else:
            print("Respuesta inválida. Por favor, responda 'si' o 'no'.")
    
    valida = False
    while not valida:
        respuesta = input("¿Ha entrado al turno algún trabajador que no pertenezca al grupo? (si/no) ").strip()
        if respuesta.lower() == "si":
            extras = input("Escribe el identificador de los trabajadores que no han asistido separados por comas: ")
            extras = [int(extra.strip()) for extra in extras.split(",")]
            valida = True
        
        elif respuesta.lower() == "no" :
            extras = []
            valida = True
        
        else:
            print("Respuesta inválida. Por favor, responda 'si' o 'no'.")
                
    return dataTable.asignar_valores_por_equipo(equipo_usuario, faltas, extras)


######### FUNCIÓN OBJETIVO #########
def funcionObjetivo(possibleSolution):
    """
    Calcula la puntuación total de la asignación, maximizando el número de máquinas operativas y
    la asignación de trabajadores con el mayor nivel de conocimiento en puestos prioritarios.
    """
    puntuacion_total = 0

    # Recorremos cada máquina o puesto (i representa la máquina o puesto)
    for i in range(dataTable.cantidad_puestos):
        
        prioridad_maquina_i = dataTable.array_Maq_Prio[i]

        # Verificamos si la máquina tiene algún trabajador asignado en 'possibleSolution'
        trabajadores_en_puesto_i = []
        for index_trab in range(dataTable.cantidad_trabajadores):
            # si el trabajador actual está en el puesto i, entonces nos guardamos el id del trabajador
            if i == possibleSolution[index_trab]:
                trabajadores_en_puesto_i.append(index_trab) 

        # Si hay algún trabajador asignado en los puestos de esta máquina, la consideramos operativa
        if any(trabajadores_en_puesto_i):  
            suma_prioridad_trabajadores = 0

            # Para cada trabajador (j representa el trabajadores dentro del puesto i)
            for index_trab_de_i in trabajadores_en_puesto_i:
                                
                prioridad_trabajador = dataTable.matriz_Prioridades[index_trab_de_i][i]

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

    puestos_no_fijos=[1,3,5,7,9,13,15]
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
                if esVecinoValido(nuevo_vecino):
                    vecinos.append(nuevo_vecino)

    return vecinos


def esVecinoValido(vecino):
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
        experiencia = dataTable.matriz_ILUO[trabajador][puesto]
        prioridad = dataTable.matriz_Prioridades[trabajador][puesto]

        # Condiciones de validez (puedes personalizar según tus reglas):
        # - Experiencia suficiente (por ejemplo, ILUO >= 3)
        # - Prioridad válida (por ejemplo, prioridad <= 3)
        if experiencia < 3 or prioridad > 3:
            return False

    return True


######### GREEDY HILL CLIMBING #########
def greedyHillClimbing(array_trabajadores_disponibles, equipo_usuario):
    """
    Implementa el algoritmo Hill Climbing para encontrar la mejor solución de la distribución de trabajadores usando la estrategia Greedy.
    """

    #Solución inicial
    bestLocalSolution = asignacionIni(equipo_usuario, array_trabajadores_disponibles)
    if not bestLocalSolution:
        return None, None
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

            print("Puntuaciones de los vecinos:", puntuaciones_vecinos)
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


######### HILL CLIMBING + TABU #########
def randomHillClimbingTabu(grupo, array_trabajadores_disponibles, tabu_list_size = 10):
    """
    Implementa el algoritmo Hill Climbing para encontrar la mejor solución de la distribución de trabajadores usando la estrategia Random.
    """

    #Solución inicial
        #asignacion anterior
    #bestLocalSolution = repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
        #asignacion actual
    bestLocalSolution = asignacionIni(grupo, array_trabajadores_disponibles)
    if not bestLocalSolution:
        return None, None
    bestGlobalSolution = bestLocalSolution
    print("Solución inicial:", bestLocalSolution)

    # Inicializar TabuList
    tabuList = []
    tabuList.append(bestLocalSolution)

    #Calcular la puntuación de la solución inicial
    bestLocalValue = funcionObjetivo(bestLocalSolution)
    bestGlobalValue = bestLocalValue
    print("Puntuación de la solución inicial:", round(bestLocalValue, 2))

    finalizado = False

    while_i = 0
    for_i = 0
    while not finalizado: 
        while_i += 1 

        #Generar los vecinos de la solución actual DE FORMA ALEATORIA
        vecinos = generarVecinos(bestLocalSolution)

        #Calcular la puntuación de los vecinos
        puntuaciones_vecinos = []
        for vecino in vecinos:
            puntuaciones_vecinos.append(funcionObjetivo(vecino))

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
def grasp(grupo, array_trabajadores_disponibles):
    """
    Implementa el algoritmo GRASP para encontrar la mejor solución de la distribución de trabajadores.
    """

    # Solución inicial
        #asignacion anterior
    #bestGlobalSolution = repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
        #asignacion actual
    bestGlobalSolution = asignacionIni(grupo, array_trabajadores_disponibles)
    if not bestGlobalSolution:
        return None, None
    bestGlobalValue = funcionObjetivo(bestGlobalSolution)
    print("Solución inicial:", bestGlobalSolution)
    print("Puntuación de la solución inicial:", round(bestGlobalValue, 2))

    finalizado = False

    while_i = 0
    while not finalizado:
        while_i += 1 
        # Generar los vecinos de la solución actual
        vecinos = generarVecinos(bestGlobalSolution)

        # Calcular la puntuación de los vecinos
        puntuaciones_vecinos = [funcionObjetivo(vecino) for vecino in vecinos]

        # Generar la Lista Restringida de Candidatos (RCL)
        rcl = grasp_generate_rcl(vecinos, puntuaciones_vecinos)

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
            print(f"Ha entrado en el while {while_i} veces")

    return bestGlobalSolution, round(bestGlobalValue, 2)

######### VND #########
def vnd(array_trabajadores_disponibles, grupo):
    """
    Implementa el algoritmo Variable Neighborhood Descent (VND) para encontrar la mejor solución.

    :param array_trabajadores_disponibles: Lista de trabajadores disponibles.
    :return: La mejor solución encontrada y su puntuación.
    """
    # vecindarios: Lista de funciones que generan vecinos para diferentes vecindarios.
    # Definir las funciones de vecindarios como una lista
    vecindarios = [
        generarVecinos,  # Vecindario 1
        generarVecinosNiveles,  # Vecindario 2
    ]

    # Solución inicial
        #asignacion anterior
    #bestGlobalSolution = repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
        #asignacion actual
    bestGlobalSolution = asignacionIni(grupo, array_trabajadores_disponibles)
    if not bestGlobalSolution:
        return None, None
    bestGlobalValue = funcionObjetivo(bestGlobalSolution)

    # print("Solución inicial:", bestGlobalSolution)
    # print("Puntuación de la solución inicial:", round(bestGlobalValue, 2))

    k = 0  # Índice del vecindario actual

    while k < len(vecindarios):
        # Generar los vecinos usando el vecindario k
        vecinos = vecindarios[k](bestGlobalSolution)

        # Calcular la puntuación de los vecinos
        puntuaciones_vecinos = [funcionObjetivo(vecino) for vecino in vecinos]

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