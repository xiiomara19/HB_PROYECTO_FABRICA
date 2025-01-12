import readTables
import itertools

######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
# Estas variables incluyen información sobre los trabajadores, los puestos disponibles, y matrices que definen prioridades y niveles de experiencia (ILUO).
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)


def asignarTL(grupo, trabajadores, sol):
    

def asignarTractorista(trabajadores, sol):

def trabajadoresPosibles(lista_puestos_ppal, trabajadores, grupo):
    puestos_y_trabajadores=[[p] for p in lista_puestos_ppal]
    for ind in range(len(lista_puestos_ppal)):
        trabajadoresPosibles = []
        puesto = lista_puestos_ppal[ind]
        for i_tr in range(cantidad_trabajadores):
            #si el trabajador está disponible
            if trabajadores[i_tr]==True :
                #si el trabajador tiene experiencia suficiente en el puesto
                if matriz_ILUO[i_tr][puesto] >= 3:
                    prio_tr_en_maq = matriz_Prioridades[i_tr][puesto]
                    pertenece_a_grupo = array_id_trabajadores[i_tr] in trabajadores_por_equipo[grupo]
                    #añadimos a trabajadoresPosibles el trabajador, su prioridad en el puesto y si pertenece al grupo
                    trabajadoresPosibles.append([i_tr, prio_tr_en_maq, pertenece_a_grupo])

        #primera posicion de cada sublista: puesto de trabajo
        #segunda posicion de cada sublista: lista de los datos del trabajador 
        puestos_y_trabajadores[ind].append(trabajadoresPosibles)

    return puestos_y_trabajadores
######### ASIGNACIÓN INICIAL #########
# Implementar una primera función que asigne trabajadores con mayor experiencia 
# (niveles 3 y 4 en la matriz ILUO) a los puestos prioritarios. 
# Los trabajadores restantes serán distribuidos usando un enfoque como el hill climbing.

def asignacionIni(grupo, trabajadores):
    puestos_principales = [0,2,4,6,8,12,14] #los puestosde TL y tractorista no se tiene en cuenta porque son casos especiales
    posibles_candidatos = []
    puestos_que_se_pueden_completar=[]
    sol = [-1] * cantidad_trabajadores
    asignarTL(grupo, trabajadores, sol)
    if array_Maq_Prio[11]==1:
        asignarTractorista(trabajadores, sol)
    
    for prio in range(1,9):
        parada = False
        #lista de los puestos principales con prioridad "prio"
        lista_puestos_ppal = [puesto for puesto in range(len(array_Maq_Prio)) if array_Maq_Prio[puesto]==prio and puesto in puestos_principales]
        posibles_candidatos=[]
        for ind, puesto in enumerate(lista_puestos_ppal):   
            #puestos_y_trabajadores es una lista de listas, donde cada sublista tiene el puesto y los trabajadores posibles para ese puesto
            puestos_y_trabajadores = trabajadoresPosibles(lista_puestos_ppal, trabajadores, grupo)
            for pri in range(1,3):
                #metemos en posibles_candidatos el indice del trabajador con prioridad "pri" y que pertenecen al grupo 
                posibles_candidatos[ind].append([sub[0] for sub in puestos_y_trabajadores[ind][1] if sub[1]==pri and sub[2]==True])
                
                if len(posibles_candidatos[ind])==0 or posibles_candidatos[ind]==None:
                    #si no hay ninguno, metemos a un trabajador con prioridad pri aunque no pertenezca al grupo 
                    posibles_candidatos[ind].append([sub[0] for sub in puestos_y_trabajadores[ind][1] if sub[1]==pri and sub[2]==False])

                #si sigue sin haber ninguno, pasamos al siguiente puesto -> nadie puede completar el puesto -> esta máquina no se puede arrancar
                if len(posibles_candidatos[ind])==0 or posibles_candidatos[ind]==None:
                    break
                #si hay alguien que pueda cubrir el puesto, lo añadimos a puestos_que_se_pueden_completar
                if len(posibles_candidatos[ind])>0:
                    puestos_que_se_pueden_completar.append(puesto)

        while not parada:
            for ind, puesto in enumerate(lista_puestos_ppal):
                #si solo hay un trabajador que pueda ocupar el puesto, lo asignamos directamente
                if len(posibles_candidatos[ind])==1:
                    trabajador = posibles_candidatos[ind][0]
                    sol[trabajador]=puesto
                    #y lo eliminamos de los los demás puestos en los que podría estar
                    for sublista in posibles_candidatos:
                        if trabajador in sublista:
                            sublista.remove(trabajador)
                #si hay más de uno
                #if len(posibles_candidatos[ind])>1:
                    #se busca si alguno de esos solamente puede cubrir ese puesto

            #primer parentesis all: si ya se han comletado todos los puestos para los que habia trabajadores => parar
            #segundo parentesis all: si no queda ningun trabajador que pueda ocupar un puesto => parar
            parada = all(sol[ind] != -1 for ind in puestos_que_se_pueden_completar) or all(posibles_candidatos[i]==[] for i in range(len(posibles_candidatos)))

    return sol

def bestFirst(puestos_y_trabajadores, lista_puestos_ppal):
    #vamos a unir a todos los trabajadores por puestos 
    datos_trabajadores=[[p] for p in lista_puestos_ppal]
    for i in len(puestos_y_trabajadores):
        for j,num in enumerate(lista_puestos_ppal):
            if puestos_y_trabajadores[i][0]==num:
                datos_trabajadores[j].append(puestos_y_trabajadores[i][1])

    
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
    valida = False
    while not valida:
        respuesta = input("¿Hay alguna falta en el equipo? (si/no)").strip()
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
        respuesta = input("¿Ha estrado al turno algún trabajador que no pertenezca al grupo? (si/no)").strip()
        if respuesta.lower() == "si":
            extras = input("Escribe el identificador de los trabajadores que no han asistido separados por comas: ")
            extras = [int(extra.strip()) for extra in extras.split(",")]
            valida = True
        
        elif respuesta.lower() == "no" :
            extras = []
            valida = True
        
        else:
            print("Respuesta inválida. Por favor, responda 'si' o 'no'.")
                
    return readTables.asignar_valores_por_equipo(trabajadores_por_equipo, equipo_usuario, cantidad_trabajadores, array_id_trabajadores, faltas, extras)


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

