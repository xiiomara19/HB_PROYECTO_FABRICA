import readTables
import itertools as iter


(array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq) = readTables.getTablesInfo(archivo)


def generarVecinos(solucion, puesots_fijos):
    """
    Genera los vecinos de la solución.
    El primer parámetro es la solución generada con hill climbing.
    El segundo parámetro es una lista con los indices de las posiciones que no
    se tienen que mover (los puestos principales de las máquinas que se van a arrancar)
    """
    vecino = []
    puestos = list(range(cantidad_puestos))
    #lista de los trabajadores del grupo que no están asignados a ningun puesto fijo
    no_fijos = [puestos[i] for i in range(cantidad_puestos) if i not in puesots_fijos]

    #ponemos los trabajadores fijos en el vecino
   # for i in range(len(arrayPosiciones)):
   #     indice = arrayPosiciones[i]
   #     vecino[indice]=arrayPosiciones[indice]
    
    return vecino_insert(solucion, no_fijos)


def vecino_insert(solucion, no_fijos):
    lista_vecinos=[]
    for i in range(cantidad_puestos)
        vecino = solucion.copy()
        elem = vecino.pop(i)
        #si el puesto no es fijo, se puede hacer insert
        if elem in por_asignar:
            primera_pos_disponible = min(por_asignar)
            vecino.insert(primera_pos_disponible, elem)



def swap(ind1, ind2, lista):
    nueva=lista.copy()
    aux=lista[ind1]
    nueva[ind1]=lista[ind2]
    nueva[ind2]=aux
    return nueva