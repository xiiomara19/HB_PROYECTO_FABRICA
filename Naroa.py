import readTables

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

def repartoTrabajadoresExperimentados(possibleSolution, cantidad_trabajadores, cantidad_puestos,array_trabajadores_disponibles, matriz_Prioridades, matriz_ILUO):
    for prio in range(1, 10):  # Itera de 1 a 9 --> Prioridades de Prio_Maq
        for cono in range(4, 0, -1):  # Itera de 4 a 1 --> Conocimientos de ILUO
            possibleSolutionNew = repartoTrabajadoresExperimentadosPrioridadConocimiento(prio, cono, possibleSolution, cantidad_trabajadores, cantidad_puestos, array_trabajadores_disponibles, matriz_Prioridades, matriz_ILUO)
            print("Possible solution after workers with experience (priority = ", prio  ,") (ILUO = ", cono, "): ", possibleSolutionNew)
    return possibleSolutionNew




# Ruta del archivo de Excel que contiene los datos
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el archivo de Excel y asignar sus valores a variables globales
# Estas variables incluyen información sobre los trabajadores, los puestos disponibles, 
# y matrices que definen prioridades y niveles de experiencia (ILUO).
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, 
 array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, 
 array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)

# Solicitar al usuario que especifique el equipo que va a trabajar.
# El equipo debe ser una letra válida entre A, B, C, D o E. 
# Cualquier otro valor se considera inválido.
equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, D, E): ").strip().upper()

# Filtrar los trabajadores disponibles según el equipo especificado.
# Esta función asigna -1 a los trabajadores que no pertenecen al equipo seleccionado.
array_trabajadores_disponibles = readTables.asignar_valores_por_equipo(
    trabajadores_por_equipo, equipo_usuario, cantidad_trabajadores, array_id_trabajadores
)
# Crear una posible solución inicial: se asignan los primeros puestos a trabajadores en orden, 
# y los trabajadores restantes se dejan sin asignar (-1).
possibleSolution = [-1 for i in range(cantidad_puestos)] + [-1 for i in range(cantidad_trabajadores - cantidad_puestos)]
print("Possible initial solution: ", possibleSolution)

possibleSolution2 = repartoTrabajadoresExperimentados(possibleSolution, cantidad_trabajadores, cantidad_puestos, array_trabajadores_disponibles, matriz_Prioridades, matriz_ILUO)
print("Possible solution after workers with experience: ", possibleSolution2)
