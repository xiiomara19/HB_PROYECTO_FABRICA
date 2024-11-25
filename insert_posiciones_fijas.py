import readTables
import math
import itertools as iter


#(array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)


# ---------------------- INSERT -------------------------
def InsertVector(V, i, j):
    #inserts hacia la derecha
    if i<=j:
        lag = V[i]
        for k in (range(i, j)):
            V[k] = V[k+1]
        V[j] = lag
        return V
    #inserts hacia la izquierda
    else:
        lag = V[i]
        for k in reversed(range(j, i+1)):
            V[k] = V[k-1]
        V[j] = lag
        return V

def calcularVecinosInsert(vectorIni): 
    N = len(vectorIni)
    vecinosInsert=set()
    for i in range(0, N):
        #inserts derecha
        for j in range(i+1, N):
            vector = vectorIni.copy()
            vectLag = InsertVector(vector,i,j)
            #es necesario que sea tupla para que sea hashable 
            # => para poder hacer el return con "vecino in vecinoInsert"
            vecinosInsert.add(tuple(vectLag))

        #inserts izquierda
        for j in range(0, i-1):
            vector = vectorIni.copy()
            vectLag = InsertVector(vector,i,j)
            vecinosInsert.add(tuple(vectLag))

    #como los valores de la lista son los puestos de trabajo y mas de un 
    #trebajador puede estar en el mismo puesto, (o sea, los numeros de la lista
    #se pueden repetir) es necesario ir eliminando las combinaciones repetidas

    #devuelve una lista con los vecinos, sin repeticiones
    return vecinosInsert


def generarVecinos(solucion, puestos_no_fijos_activos):
    """
    Genera los vecinos de la solución.
    El primer parámetro es la solución generada con hill climbing.
    El segundo parámetro es una lista con los indices de las posiciones que no
    necesitan un nivel específico (los puestos secundarios de las máquinas que se van a arrancar)
    """
    lista_vecinos=[]
    subvecinos=set()
    plantilla = solucion.copy()
    #creamos una lista con los trabajadores en los puestos fijos,
    #los puestos que podamos ir cambiando tendran valor inf
    plantilla = [float('inf') if elemento in puestos_no_fijos_activos else elemento for elemento in solucion]
    
    #generar todas las asignaciones posibles 
    subvecinos=calcularVecinosInsert(puestos_no_fijos_activos)

    for elem in subvecinos:
        elem_iter = iter(elem)
        vecino=plantilla.copy()
        for i in range(len(plantilla)):
            if plantilla[i] == float('inf'):  # Verifica si el valor es inf
                try: 
                    vecino[i] = next(elem_iter)  # Toma el siguiente elemento de elem
                except StopIteration:
                    break  
        lista_vecinos.append(vecino)
    
    return lista_vecinos
    


