import readTables
import main

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


def main_program():
    # Solicitar al usuario el equipo al que pertenece su equipo con control de errores
    intentos = 0
    while intentos < 4:
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, D, E): ").strip().upper()
        # Verificar si el equipo ingresado es válido
        if equipo_usuario in ['A', 'B', 'C', 'D', 'E']:
            # Obtener los valores asignados por el equipo
            print("Equipo seleccionado: ", equipo_usuario)
            array_trabajadores_disponibles = readTables.asignar_valores_por_equipo(trabajadores_por_equipo, equipo_usuario, cantidad_trabajadores, array_id_trabajadores)
        
            # Mostrar el resultado
            print("Trabajadores disponibles: ")
            print(array_trabajadores_disponibles)
            print("Terminado")
            #Salir del while
            break
        else:
            print("Error: Entrada inválida. Por favor, ingrese uno de los equipos válidos: A, B, C, D, E.")
            intentos += 1

    if intentos == 4:
        print("Ha superado el número de intentos fallidos. Vuelva a intentarlo más tarde.")

if __name__ == "__main__":
    main_program()