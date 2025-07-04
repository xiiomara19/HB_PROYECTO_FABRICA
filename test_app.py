import main
import table

######### DATOS INICIALES #########
# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'
# Crear una instancia de la clase Table
tabla = table.Table(archivo)

def main_program(numprueba):
    if numprueba == 1:
        print("---------------------------------------CONTENIDO EXCEL---------------------------------------")
        #Imprimir las variables globales para confirmar que no ha habido ningún problema
        tabla.getAttributes()

    elif numprueba == 2:
        """PRUEBAS FUNCIÓN OBJETIVO"""
        print("---------------------------------------PRUEBAS FUNCIÓN OBJETIVO---------------------------------------")
        # Coger en orden los trabajadores hasta llenar todos los puestos:
        # si el el array[0] = 1 significa que el trabajador 0 (id = 13512) trabaja en el puesto numero 1 (AB1 Ayte)
        possibleSolution1 = [i for i in range(tabla.cantidad_puestos)] + [-1 for i in range(tabla.cantidad_trabajadores - tabla.cantidad_puestos)]
        print("Possible solutuion 1: ", possibleSolution1)
        # Ejemplo de uso con datos ficticios
        puntuacion = main.funcionObjetivo(possibleSolution1)
        print("Puntuación total:", puntuacion)


        # CASO REAL ASGINACIONES EXCEL:
        # si el el array[0] = 1 significa que el trabajador 0 (id = 13512) trabaja en el puesto numero 1 (AB1 Ayte)
        possibleSolution2 = [-1 for i in range(tabla.cantidad_trabajadores)]
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
        possibleSolution3 = [-1 for i in range(tabla.cantidad_trabajadores)]
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
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, E): ").strip().upper()

        # Filtrar los trabajadores disponibles según el equipo especificado.
        # Esta función asigna -1 a los trabajadores que no pertenecen al equipo seleccionado.
        array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)

        possibleSolution = main.repartoTrabajadoresExperimentados(array_trabajadores_disponibles)
        print("Possible solution after workers with experience: ", possibleSolution)

    elif numprueba == 4:
        """PRUEBAS INSERT"""
        print("---------------------------------------PRUEBAS INSERT---------------------------------------")
        print(main.generarVecinos([1,2,3,4,5]))
        #respuestas esperadas: [3,2,1,4,5], [3,2,5,4,1], [1,2,5,4,3], [5,2,1,4,3]
        print(main.generarVecinos([6,1,1,2,10,5]))
        #respuestas esperadas: [6,1,5,2,10], [6,5,1,2,10,1], [6,1,1,2,10,5]

        #print(conseguirPuestosNoFijosActivos([1,2,2,3],[2]))

    elif numprueba == 5:
        """PRUEBAS HILL CLIMBING"""
        print("---------------------------------------PRUEBAS HILL CLIMBING---------------------------------------")
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, E): ").strip().upper()
        array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)

        # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
        solution, value = main.greedyHillClimbing(array_trabajadores_disponibles, equipo_usuario)
        if solution is None or  value is None:
            print("No se encontró una solución con el equipo", equipo_usuario)
        else:
            print("La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value)

    elif numprueba == 6:
        """PRUEBAS GRASP"""
        print("---------------------------------------PRUEBAS GRASP---------------------------------------")
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, E): ").strip().upper()
        array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)

        # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
        solution, value = main.grasp(equipo_usuario, array_trabajadores_disponibles)
        if solution is None or  value is None:
            print("No se encontró una solución con el equipo", equipo_usuario)
        else:
            print("La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value)
    
    elif numprueba == 7:
        """PRUEBAS randomHillClimbingTabu"""
        print("---------------------------------------PRUEBAS RANDOM HILL CLIMBING CON TABU SEARCH---------------------------------------")
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, E): ").strip().upper()
        array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)

        # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
        solution, value = main.randomHillClimbingTabu(equipo_usuario, array_trabajadores_disponibles)
        if solution is None or  value is None:
            print("No se encontró una solución con el equipo", equipo_usuario)
        else:
            print("La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value)
    
    elif numprueba == 8:
        """PRUEBAS VND"""
        print("---------------------------------------PRUEBAS VND---------------------------------------")
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, E): ").strip().upper()
        array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)

        # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
        solution, value = main.vnd(array_trabajadores_disponibles, equipo_usuario)
        if solution is None or  value is None:
            print("No se encontró una solución con el equipo", equipo_usuario)
        else:
            print("La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value)
    


    elif numprueba == 9:
        """PRUEBAS CLASE TABLE"""
        print("---------------------------------------PRUEBAS CLASE TABLE---------------------------------------")
        
        # Comrpobamos que se hayan inicializado bien los atributos de dos formas
        #1. Usando el método getAttributes
        print("Imprimiendo los atributos con el método getAttributes:")
        tabla.getAttributes()
        #2. Imprimiendo los atributos uno por uno
        print("\nImprimiendo los atributos uno por uno:")
        print("\nTrabajadores por equipo:\n", tabla.trabajadores_por_equipo)
        print("\nId de trabajadores:\n",tabla.array_id_trabajadores)
        print("\nCantidad de trabajadores:\n",tabla.cantidad_trabajadores)
        print("\nPuestos de trabajo:\n",tabla.array_puestos_de_trabajo)
        print("\nCantidad de puestos:\n",tabla.cantidad_puestos)
        print("\nMatriz ILUO:\n",tabla.matriz_ILUO)
        print("\nMatriz Prioridades:\n",tabla.matriz_Prioridades)
        print("\nArray Maq Prio:\n",tabla.array_Maq_Prio)
        print("\nArray OP Maq:\n",tabla.array_OP_Maq)


if __name__ == "__main__":
    print("¿Qué pruebas de que función quieres ejecutar?")
    numprueba = int(input("1. Visualizar contenido excel\n"
                          "2. Pruebas de función objetivo\n"
                          "3. Pruebas de asignación inicial\n"
                          "4. Pruebas insert\n"
                          "5. Pruebas Hill Climbing\n"
                          "6. Pruebas GRASP\n"
                          "7. Pruebas randomHillClimbingTabu\n"
                          "8. Pruebas VND\n"
                          "9. Pruebas clase Table\n"))
    main_program(numprueba)

