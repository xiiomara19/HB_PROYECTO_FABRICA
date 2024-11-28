import readTables
import main

######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'

# Leer el excel y asígnarlo a variables globales
# Estas variables incluyen información sobre los trabajadores, los puestos disponibles, y matrices que definen prioridades y niveles de experiencia (ILUO).
(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)


def main_program(numprueba):
    if numprueba == 1:
        print("---------------------------------------CONTENIDO EXCEL---------------------------------------")
        #Imprimir las variables globales para confirmar que no ha habido ningún problema
        readTables.printTablesInfo(trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) 

    elif numprueba == 2:
        """PRUEBAS FUNCIÓN OBJETIVO"""
        print("---------------------------------------PRUEBAS FUNCIÓN OBJETIVO---------------------------------------")
        # Coger en orden los trabajadores hasta llenar todos los puestos:
        # si el el array[0] = 1 significa que el trabajador 0 (id = 13512) trabaja en el puesto numero 1 (AB1 Ayte)
        possibleSolution1 = [i for i in range(cantidad_puestos)] + [-1 for i in range(cantidad_trabajadores - cantidad_puestos)]
        print("Possible solutuion 1: ", possibleSolution1)
        # Ejemplo de uso con datos ficticios
        puntuacion = main.funcionObjetivo(possibleSolution1)
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
        puntuacion = main.funcionObjetivo(possibleSolution2)
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
        puntuacion = main.funcionObjetivo(possibleSolution3)
        print("Puntuación total:", puntuacion)


        # Caso preguntando qué equipo viene a trabajar, asignandoles -1 al resto de valores:
        # si el el array[0] = 1 significa que el trabajador 0 (id = 13512) trabaja en el puesto numero 1 (AB1 Ayte)

        
    elif numprueba == 3:
        """PRUEBAS ASIGNACIÓN INICIAL"""
        print("---------------------------------------PRUEBAS ASIGNACIÓN INICIAL---------------------------------------")
        # Solicitar al usuario que especifique el equipo que va a trabajar.
        # El equipo debe ser una letra válida entre A, B, C, D o E. 
        # Cualquier otro valor se considera inválido.
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, D, E): ").strip().upper()

        # Filtrar los trabajadores disponibles según el equipo especificado.
        # Esta función asigna -1 a los trabajadores que no pertenecen al equipo seleccionado.
        array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)
        # Crear una posible solución inicial: se asignan los primeros puestos a trabajadores en orden, 
        # y los trabajadores restantes se dejan sin asignar (-1).
        possibleSolution = [-1 for i in range(cantidad_puestos)] + [-1 for i in range(cantidad_trabajadores - cantidad_puestos)]
        print("Possible initial solution: ", possibleSolution)

        possibleSolution2 = main.repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
        print("Possible solution after workers with experience: ", possibleSolution2)

    elif numprueba == 4:
        """PRUEBAS INSERT"""
        print("---------------------------------------PRUEBAS INSERT---------------------------------------")
        print(main.generarVecinos([1,2,3,4], [3,2,1]))
        #respuestas esperadas: [2,1,3,4], [2,3,1,4] [1,3,2,4] [3,1,2,4]
        print(main.generarVecinos([6,1,2,5,6,7], [5,2,7]))
        #respuestas esperadas: [6,1,2,5,6,7], [6,1,2,7,6,5], [6,1,5,7,6,2], [6,1,7,5,6,2]
        print(main.generarVecinos([6,1,2,5,6,2], [5,2]))
        #respuestas esperadas: [6,1,2,2,6,5], [6,1,5,2,6,2], [6,1,2,5,6,2]

        #print(valores([1,2,2,3],[2]))

if __name__ == "__main__":
    print("¿Qué pruebas de que función quieres ejecutar?")
    numprueba = int(input("1. Visualizar contenido excel\n2. Pruebas de función objetivo\n3. Pruebas de asignación inicial\n4. Pruebas insert\n"))
    main_program(numprueba)

