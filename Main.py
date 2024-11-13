import readTables

######### FUNCIÓN OBJETIVO #########

def funcionObjetivo(possibleSolution):
    """
    Calcula la puntuación total de la asignación, maximizando el número de máquinas operativas y
    la asignación de trabajadores con el mayor nivel de conocimiento en puestos prioritarios.
    """
    puntuacion_total = 0

    # Recorremos cada máquina o puesto (i representa la máquina o puesto)
    for i in range(cantidad_puestos):
        # print("MAQUINA I =", i)
        
        prioridad_maquina_i = array_Maq_Prio[i]

        # Verificamos si la máquina tiene algún trabajador asignado en 'possibleSolution'
        trabajadores_en_puesto_i = []
        for index_trab in range(cantidad_trabajadores):
            # si el trabajador actual está en el puesto i, entonces nos guardamos el id del trabajador
            if i == possibleSolution[index_trab]:
                trabajadores_en_puesto_i.append(index_trab) 

        # print("trabajadores_en_puesto_i = ", trabajadores_en_puesto_i)
        # Si hay algún trabajador asignado en los puestos de esta máquina, la consideramos operativa
        if any(trabajadores_en_puesto_i):  
            suma_prioridad_trabajadores = 0

            # Para cada trabajador (j representa el trabajadores dentro del puesto i)
            for index_trab_de_i in trabajadores_en_puesto_i:
                # print("index_trab_de_i = ", index_trab_de_i)
                                
                prioridad_trabajador = matriz_Prioridades[index_trab_de_i][i]

                # Añadir a la puntuación de la máquina con el inverso de las prioridades
                suma_prioridad_trabajadores += 1 / prioridad_trabajador

            # Ponderar la puntuación de la máquina con el inverso de la prioridad de la máquina
            puntuacion_total += (1 / prioridad_maquina_i) * suma_prioridad_trabajadores

    return puntuacion_total


######### MAIN #########


# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)

#Imprimir las variables globales para confirmar que no ha habido ningún problema
readTables.printTablesInfo(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) 

# Coger en orden los trabajadores hasta llenar todos los puestos:
# si el el array[0] = 1 significa que el trabajador 0 (id = 13512) trabaja en el puesto numero 1 (AB1 Ayte)
possibleSolution1 = [i for i in range(cantidad_puestos)] + [-1 for i in range(cantidad_trabajadores - cantidad_puestos)]
print("Possible solutuion 1: ", possibleSolution1)
# Ejemplo de uso con datos ficticios
puntuacion = funcionObjetivo(possibleSolution1)
print("Puntuación total:", puntuacion)


# CASO REAL ASGINACIONES EXCEL:
# si el el array[0] = 1 significa que el trabajador 0 (id = 13512) trabaja en el puesto numero 1 (AB1 Ayte)
possibleSolution2 = [-1 for i in range(cantidad_trabajadores)]
possibleSolution2[72] = 0
possibleSolution2[73] = 1
possibleSolution2[66] = 2
possibleSolution2[62] = 3
possibleSolution2[68] = 4
possibleSolution2[64] = 5
possibleSolution2[70] = 6
possibleSolution2[71] = 7
possibleSolution2[60] = 8
possibleSolution2[63] = 9
possibleSolution2[77] = 10
possibleSolution2[65] = 11
possibleSolution2[76] = 12
possibleSolution2[74] = 13
possibleSolution2[78] = 13
possibleSolution2[75] = 14
possibleSolution2[71] = 15
print("Possible solutuion 2: ", possibleSolution2)
# Ejemplo de uso con datos ficticios
puntuacion = funcionObjetivo(possibleSolution2)
print("Puntuación total:", puntuacion)


# Caso artifical para comprobar la suma de función objetivo:
# si el el array[0] = 1 significa que el trabajador 0 (id = 13512) trabaja en el puesto numero 1 (AB1 Ayte)
possibleSolution3 = [-1 for i in range(cantidad_trabajadores)]
possibleSolution3[38] = 0
possibleSolution3[0] = 0
possibleSolution3[1] = 1
possibleSolution3[2] = 1

print("Possible solutuion 3: ", possibleSolution3)
# Ejemplo de uso con datos ficticios
puntuacion = funcionObjetivo(possibleSolution3)
print("Puntuación total:", puntuacion)




