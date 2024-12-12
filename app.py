import main
import GRASP
import HillClimbingTabu

def main_program(equipo_usuario):
    # Obtener los valores asignados por el equipo
    array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)

    print("--------------------- GREEDY HILL CLIMBING ---------------------")
    # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
    solution, value = main.greedyHillClimbing(array_trabajadores_disponibles)
    print("GREEDY HILL CLIMBING: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")

    print("--------------------- GRASP ---------------------------")
    # GRASP devuelve la mejor solución de la distribución de trabajadores
    solution, value = GRASP.grasp(array_trabajadores_disponibles)
    print("GRASP: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")

    print("--------------------- RANDOM HILL CLIMBING + TABU LIST ---------------------")
    # Hill Climbing con Tabu List devuelve la mejor solución de la distribución de trabajadores
    tabu_list_size = 10
    solution, value = HillClimbingTabu.randomHillClimbingTabu(array_trabajadores_disponibles, tabu_list_size)
    print("RANDOM HILL CLIMBING + TABU LIST: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")

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