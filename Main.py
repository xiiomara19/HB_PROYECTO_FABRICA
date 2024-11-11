import readTables

######### FUNCIÓN OBJETIVO #########

def funcionObjetivo():
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
                trabajadores_en_puesto_i.append(possibleSolution[index_trab]) 

        # Si hay algún trabajador asignado en los puestos de esta máquina, la consideramos operativa
        if any(trabajadores_en_puesto_i):  
            suma_prioridad_trabajadores = 0

            # Para cada trabajador (j representa el trabajadores dentro del puesto i)
            for j, id_trabajador_asignado_en_i in enumerate(trabajadores_en_puesto_i):
                
                prioridad_trabajador = matriz_Prioridades[i][j]

                # Añadir a la puntuación de la máquina con el inverso de las prioridades
                suma_prioridad_trabajadores += 1 / prioridad_trabajador

            # Ponderar la puntuación de la máquina con el inverso de la prioridad de la máquina
            puntuacion_total += (1 / prioridad_maquina_i) * suma_prioridad_trabajadores

    return puntuacion_total


######### MAIN #########


# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
(array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)

#Imprimir las variables globales para confirmar que no ha habido ningún problema
readTables.printTablesInfo(array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) 

# Coger en orden los trabajadores hasta llenar todos los puestos:
# si el el array[0] = 1 significa que el trabajador 0 (id = 13512) trabaja en el puesto numero 1 (AB1 Ayte)
possibleSolution = [1 for i in range(cantidad_puestos)] + [0 for i in range(cantidad_trabajadores - cantidad_puestos)]

# Ejemplo de uso con datos ficticios
# Suponiendo que array_Maq_Prio, matriz_Prioridades, possibleSolution, y cantidad_puestos están definidos en el entorno.
puntuacion = funcionObjetivo()
print("Puntuación total:", puntuacion)
