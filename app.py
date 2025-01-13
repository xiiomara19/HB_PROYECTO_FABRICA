import GRASP
import HillClimbingTabu
import main
import VND

def main_program(array_trabajadores_disponibles):

    # Obtener los valores asignados por el equipo
    array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)


    print("--------------------- GREEDY HILL CLIMBING ---------------------")
    # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
    solution, value = main.greedyHillClimbing(array_trabajadores_disponibles)
    print("GREEDY HILL CLIMBING: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")

    print("--------------------- Greedy randomized adaptive search procedure (GRASP) ---------------------------")
    # GRASP devuelve la mejor solución de la distribución de trabajadores
    rcl_size = 3  # Entre cuantos mejores vecinos hacer random choice el GRASP
    solution, value = GRASP.grasp(array_trabajadores_disponibles, rcl_size)
    print("GRASP: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")

    print("--------------------- RANDOM HILL CLIMBING + TABU LIST ---------------------")
    # Hill Climbing con Tabu List devuelve la mejor solución de la distribución de trabajadores
    tabu_list_size = 10
    solution, value = HillClimbingTabu.randomHillClimbingTabu(array_trabajadores_disponibles, tabu_list_size)
    print("RANDOM HILL CLIMBING + TABU LIST: \n La mejor distribución de trabajadores del equipo", equipo_usuario, "sería: ", solution, '\n con un valor de:', value, "\n")

    print("--------------------- Variable Neighborhood Descent (VND) ---------------------")
    # VND devuelve la mejor solución de la distribución de trabajadores
    solution, value = VND.vnd(array_trabajadores_disponibles)
    print("VND: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")

    # # Hill Climbing con Tabu List devuelve la mejor solución de la distribución de trabajadores
    # solution, value = HillClimbingTabu.greedyHillClimbingTabu(array_trabajadores_disponibles)
    # print("GREEDY HILL CLIMBING + TABU LIST: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value)

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