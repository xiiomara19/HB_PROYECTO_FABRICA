import main
import matplotlib.pyplot as plt
import time
import statistics
import numpy as np

def crearGraficosTiempos(tiempos, funciones, equipo_usuario):
    plt.bar(funciones, tiempos)
    plt.xlabel("Funciones")
    plt.ylabel("Tiempo (s)")
    plt.grid(True)
    plt.title("Comparación tiempo de ejecución. Equipo " + equipo_usuario)
    plt.show()

def crearGraficosResultados(resultados, funciones, equipo_usuario):
    plt.plot(funciones, resultados, marker='o', linestyle='-')
    plt.xlabel("Funciones")
    plt.ylabel("Valor resultado")
    plt.ylim(0,max(resultados)+1.1)
    plt.yticks(np.arange(0, max(resultados)+1.1, 0.5))
    plt.grid(True)
    plt.title("Comparación de resultados. Equipo " + equipo_usuario)
    plt.show()

def main_program(array_trabajadores_disponibles):
    #valor de iter con el que se han hecho los graficos: 30
    iter=1 #pongo uno para no tener que borrar lo sñadido para conseguir las medias para los graficos
    resultados=[]
    tiempos=[]
    funciones=["greedy hill-climbing","grasp","random hill-climbing + tabu","vnd"]
    # Obtener los valores asignados por el equipo
    array_trabajadores_disponibles = main.asignar_valores_por_equipo(equipo_usuario)


    print("--------------------- GREEDY HILL CLIMBING ---------------------")
    # Hill Climbing devuelve la mejor solución de la distribución de trabajadores
    t=[]
    r=[]
    for i in range(iter):
        inicio = time.perf_counter()
        solution, value = main.greedyHillClimbing(array_trabajadores_disponibles, equipo_usuario)
        fin = time.perf_counter()
        t.append(fin - inicio)
        if solution is None or value is None:
            print("No se encontró una solución con el equipo", equipo_usuario)
            r.append(0)
        else:
            print("GREEDY HILL CLIMBING: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")
            r.append(value)
    media = statistics.mean(t)
    if not all(elem==0 for elem in r):
        print(r)
        mr=statistics.mean(r)
    else: mr=0
    resultados.append(mr)
    tiempos.append(media)
    print("--------------------- Greedy randomized adaptive search procedure (GRASP) ---------------------------")
    # GRASP devuelve la mejor solución de la distribución de trabajadores
    t=[]
    r=[]
    for i in range(iter):
        inicio = time.perf_counter()
        solution, value = main.grasp(equipo_usuario, array_trabajadores_disponibles)
        fin = time.perf_counter()
        t.append(fin - inicio)
        if solution is None or  value is None:
            print("No se encontró una solución con el equipo", equipo_usuario)
            r.append(0)
        else:
            print("GRASP: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")
            r.append(value)
    media = statistics.mean(t)
    if not all(elem==0 for elem in r):
        mr=statistics.mean(r)
    else: mr=0
    resultados.append(mr)
    tiempos.append(media)

    print("--------------------- RANDOM HILL CLIMBING + TABU LIST ---------------------")
    # Hill Climbing con Tabu List devuelve la mejor solución de la distribución de trabajadores
    t=[]
    r=[]
    for i in range(iter):
        inicio = time.perf_counter()
        solution, value = main.randomHillClimbingTabu(equipo_usuario, array_trabajadores_disponibles)
        fin = time.perf_counter()
        t.append(fin - inicio)
        if solution is None or  value is None:
            print("No se encontró una solución con el equipo", equipo_usuario)
            r.append(0)
        else:
            print("RANDOM HILL CLIMBING + TABU LIST: \n La mejor distribución de trabajadores del equipo", equipo_usuario, "sería: ", solution, '\n con un valor de:', value, "\n")
            r.append(value)

    media = statistics.mean(t)
    if not all(elem==0 for elem in r):
        mr=statistics.mean(r)
    else: mr=0
    resultados.append(mr)
    tiempos.append(media)

    print("--------------------- Variable Neighborhood Descent (VND) ---------------------")
    # VND devuelve la mejor solución de la distribución de trabajadores
    t=[]
    r=[]
    for i in range(iter):
        inicio = time.perf_counter()
        solution, value = main.vnd(array_trabajadores_disponibles, equipo_usuario)
        fin = time.perf_counter()
        t.append(fin - inicio)
        if solution is None or  value is None:
            print("No se encontró una solución con el equipo", equipo_usuario)
            r.append(0)
        else:
            print("VND: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value, "\n")
            r.append(value)
    media = statistics.mean(t)
    if not all(elem==0 for elem in r):
        mr=statistics.mean(r)
    else: mr=0
    resultados.append(mr)
    tiempos.append(media)

   # crearGraficosTiempos(tiempos, funciones, equipo_usuario)
   # crearGraficosResultados(resultados, funciones, equipo_usuario)

    # # Hill Climbing con Tabu List devuelve la mejor solución de la distribución de trabajadores
    # solution, value = HillClimbingTabu.greedyHillClimbingTabu(array_trabajadores_disponibles)
    # print("GREEDY HILL CLIMBING + TABU LIST: La mejor distribución de trabajadores del equipo", equipo_usuario, "sería:\n", solution, '\ncon un valor de:', value)

if __name__ == "__main__":
    # Solicitar al usuario el equipo al que pertenece su equipo con control de errores
    intentos = 0
    while intentos < 4:
        equipo_usuario = input("Introduce el equipo de tu preferencia (A, B, C, E): ").strip().upper()
        # Verificar si el equipo ingresado es válido
        if equipo_usuario in ['A', 'B', 'C', 'E']:
            main_program(equipo_usuario)
            #Salir del while
            break
        else:
            print("Error: Entrada inválida. Por favor, ingrese uno de los equipos válidos: A, B, C, E.")
            intentos += 1

    if intentos == 4:
        print("Ha superado el número de intentos fallidos. Vuelva a intentarlo más tarde.")

