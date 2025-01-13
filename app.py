import main

def main_program(equipo_usuario):
    # Obtener los valores asignados por el equipo
    array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)

    # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
    solution, value = main.greedyHillClimbing(array_trabajadores_disponibles, equipo_usuario)
    print("La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value)


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

        