import main

def main_program(array_trabajadores_disponibles):

    # Obtener los valores asignados por el equipo
    array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)

    print("--------------------- GREEDY HILL CLIMBING ---------------------")
    # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
    title = "GREEDY HILL CLIMBING"
    output_filename = title + ".xlsm"
    solution, value = main.greedyHillClimbing(array_trabajadores_disponibles)
    main.printResultado(title, equipo_usuario, solution, value)
    main.exportResultadoToExcel(title, equipo_usuario, solution, value, output_filename)

    print("--------------------- Greedy randomized adaptive search procedure (GRASP) ---------------------------")
    # GRASP devuelve la mejor solución de la distribución de trabajadores
    title = "GRASP"
    output_filename = title + ".xlsm"
    rcl_size = 3  # Entre cuantos mejores vecinos hacer random choice el GRASP
    solution, value = main.grasp(array_trabajadores_disponibles, rcl_size)
    main.printResultado(title, equipo_usuario, solution, value)
    main.exportResultadoToExcel(title, equipo_usuario, solution, value, output_filename)

    print("--------------------- RANDOM HILL CLIMBING + TABU LIST ---------------------")
    # Hill Climbing con Tabu List devuelve la mejor solución de la distribución de trabajadores
    title = "RANDOM HILL CLIMBING + TABU LIST"
    output_filename = title + ".xlsm"
    tabu_list_size = 10
    solution, value = main.randomHillClimbingTabu(array_trabajadores_disponibles, tabu_list_size)
    main.printResultado(title, equipo_usuario, solution, value)
    main.exportResultadoToExcel(title, equipo_usuario, solution, value, output_filename)

    print("--------------------- Variable Neighborhood Descent (VND) ---------------------")
    # VND devuelve la mejor solución de la distribución de trabajadores
    title = "VND"
    output_filename = title + ".xlsm"
    solution, value = main.vnd(array_trabajadores_disponibles)
    main.printResultado(title, equipo_usuario, solution, value)
    main.exportResultadoToExcel(title, equipo_usuario, solution, value, output_filename)

if __name__ == "__main__":
    # Solicitar al usuario el equipo al que pertenece su equipo con control de errores
    intentos = 0
    while intentos < 4:
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, D, E): ").strip().upper()
        # Verificar si el equipo ingresado es válido
        if equipo_usuario in ['A', 'B', 'C', 'D', 'E']:
            main_program(equipo_usuario)
            #Salir del while
            break
        else:
            print("Error: Entrada inválida. Por favor, ingrese uno de los equipos válidos: A, B, C, D, E.")
            intentos += 1

    if intentos == 4:
        print("Ha superado el número de intentos fallidos. Vuelva a intentarlo más tarde.")