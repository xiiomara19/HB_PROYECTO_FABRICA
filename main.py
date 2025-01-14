import readTables
import itertools

######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
# Estas variables incluyen información sobre los trabajadores, los puestos disponibles, y matrices que definen prioridades y niveles de experiencia (ILUO).
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)

#TODO: revisar asignacion TL
#TODO: hacer que la aplicacion pare si no hay team leader
def asignarTL(grupo, trabajadores, sol):
    for ind in range(cantidad_trabajadores):
        print(ind)
        if trabajadores[ind] and matriz_Prioridades[ind][10]==1 and array_id_trabajadores[ind] in trabajadores_por_equipo[grupo]:
            sol[ind]=10
            print("TL = ", ind)
            break
    
    print("ERROR: no hay team leader para el turno")

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
    sol1 = [-1 for i in range(cantidad_trabajadores)]

    asignarTL(grupo, trabajadores, sol1)
    #asignamos los puestos principales
    asignacionIniPuestosPpal(grupo, trabajadores, sol1)
    #asignamos los puestos secundarios
    asignacionIniPuestosSec(trabajadores, sol1)

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

    print("=====================================")
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
                    if array_id_trabajadores[puesto]==prio: 
                        if puesto == 11 and sol.count(11)<2 and matriz_ILUO[tr][11]>0:
                            sol[tr]=11
                        elif puesto != 11 and matriz_ILUO[tr][puesto]>0:
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
        lista_puestos_ppal = [puesto for puesto in range(len(array_Maq_Prio)) if array_Maq_Prio[puesto]==prio and puesto in puestos_principales]
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

    for tr in range(cantidad_trabajadores):
        if trabajadores[tr] and sol[tr]==-1:
            for puesto in puestos_sec:
                #si el trabajador puede ocupar ese puesto (ILUO>0),
                #el puesto principal de la maquina esta ocupado,
                #el trabajador no esta ya en un puesto
                #y el puesto secundario esta sin asignar
                if matriz_ILUO[tr][puesto]>0 and puesto-1 in sol and puesto not in sol:
                    #asignamos el puesto secundario
                    sol[tr]=puesto
                    break
    print("solucion con asignacion de puestos secundarios: ", sol)

#TODO: revisar
def funcionObjetiboAsignacionIni(sol, grupo):
    val = 0
    for trabajador in range(len(sol)):
        puesto=sol[trabajador]
        #por cada puesto activo, se suma la prioridad del trabajador en la máquina y un plus si pertenece al grupo
        if puesto != -1:
            prioridad_trabajador_en_maquina = matriz_Prioridades[trabajador][puesto]
            pertenece_a_grupo = array_id_trabajadores[trabajador] in trabajadores_por_equipo[grupo]
            #asignar trabajadores que pertenecen al grupo es más importante, por eso se le da más peso
            #pero el peso que se le añade no puede ser superior a la prioridad del trabajador en la máquina
            if pertenece_a_grupo:
                val +=( 1/prioridad_trabajador_en_maquina) + 0.1
            else:
                val += 1/(prioridad_trabajador_en_maquina)

    return val

#TODO: crear funcion generarCombinaciones
def generarCombinaciones(puestos_y_trabajadores):
    combs=[]
    for i in range(len(puestos_y_trabajadores)):
        puesto = puestos_y_trabajadores[i][0]
       # for j in puestos_y_trabajadores[i][1:]:
            

    return combs

#TODO: crear funcion asignar
def asignar(comb):
    sol=[]

    return sol
    

def bestFirst(puestos_y_trabajadores, grupo, sol):
    #asumimos que la primera solucion es la mejor
    val_mejor_sol = funcionObjetiboAsignacionIni(sol,grupo)
    mejor_sol = sol.copy()
    val_sol = float('-inf')
    solucion = []
    #generamos todas las combinaciones de trabajadores y puestos posibles
    combinaciones = generarCombinanciones(puestos_y_trabajadores, grupo)
    #combinaciones es una lista de tuplas con esta estructura: (puesto, [id_trabajadores])
    for comb in combinaciones:
        solucion = asignar(comb)
        val_sol = funcionObjetiboAsignacionIni(solucion,puestos_y_trabajadores)
        if val_sol > val_mejor_sol:
            return solucion

    return mejor_sol

    
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

    puestos_no_fijos=[1,3,5,7,9,13,15]
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
def greedyHillClimbing(array_trabajadores_disponibles, equipo):
    """
    Implementa el algoritmo Hill Climbing para encontrar la mejor solución de la distribución de trabajadores usando la estrategia Greedy.
    """

    #Solución inicial
    #bestLocalSolution = repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
    bestLocalSolution = asignacionIni(equipo, array_trabajadores_disponibles)
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

