import pandas as pd
"""
readTables.py

Este módulo contiene funciones para extraer y procesar información específica de un archivo de Excel,
organizado en varias hojas de datos relacionadas con trabajadores, puestos de trabajo, matrices de prioridad, 
y asignaciones de operadores por máquina.

Requisitos:
- pandas
- openpyxl

Instalación de dependencias (si es necesario):
```shell
pip install pandas
pip install openpyxl
"""

####### GET EQUIPOS DE TRABAJADORES ########3
def getTrabajadoresPorEquipo(archivo):
    # Representación de los equipos y sus trabajadores en un diccionario
    # trabajadores_por_equipo = {
    # "A": [13512, 13924, 13532, 13291, 11865, 13923, 11358, 10308, 13542, 10612, 10694, 10361, 9022, 11252, 12156, 10316, 7741, 12536],
    # "B": [9729, 13297, 7680, 10693, 10354, 13921, 13346, 13932, 13677, 12418, 11132, 13968, 9362, 13679, 10590, 8879, 11360, 13468],
    # "C": [13404, 10698, 12227, 13922, 9843, 10591, 12023, 10313, 13242, 13964, 7470, 13962, 12374, 13930, 7468, 13866, 10472, 10889, 13652, 8877, 11002],
    # "D": [12422, 8210, 13241],
    # "E": [11983, 12228, 9017, 9844, 9225, 8921, 8882]}

    # Leer las columnas por nombre, no por letras (Eq para equipos y Npers para IDs de trabajadores)
    df = pd.read_excel(archivo, sheet_name='ILUO', usecols=["Eq", "Npers"])

    # Crear un diccionario vacío para almacenar los trabajadores por equipo
    trabajadores_por_equipo = {}

    # Iterar sobre las filas del DataFrame
    for _, row in df.iterrows():
        equipo = row['Eq']  # Columna Eq: equipo
        id_trabajador = row['Npers']  # Columna Npers: ID del trabajador
        
        # Si el equipo no existe en el diccionario, lo agregamos
        if equipo not in trabajadores_por_equipo:
            trabajadores_por_equipo[equipo] = []
        
        # Agregar el ID del trabajador a la lista correspondiente al equipo
        trabajadores_por_equipo[equipo].append(id_trabajador)

    return trabajadores_por_equipo


######### IDs DE TRABAJADORES #########
def getIdTrabajadores(archivo):
    """
    Extrae los IDs de trabajadores desde la columna B de la hoja "ILUO" del archivo.
    """
    # Leer solo la columna B de la hoja "ILUO"
    df_id_trabajadores = pd.read_excel(archivo, sheet_name='ILUO', usecols="B")

    # Convertir todos los valores a integer
    df_id_trabajadores = df_id_trabajadores.fillna(0).astype(int)

    # Convertir la columna en una lista (array de una sola columna)
    return df_id_trabajadores.squeeze().tolist()

######### PUESTOS DE TRABAJO #########
def getPuestosDeTrabajo(archivo):
    """
    Extrae los puestos de trabajo de la primera fila, columnas C a S, en la hoja "ILUO".
    """
    # Leer solo la primera fila de las columnas C a S en la hoja "ILUO"
    df_puestos_trabajo = pd.read_excel(archivo, sheet_name='ILUO', usecols="C:R", nrows=1, header=None)

    # Convertir todos los valores a tipo string
    df_puestos_trabajo = df_puestos_trabajo.astype(str)

    # Convertir el DataFrame en una lista (array)
    return df_puestos_trabajo.values.flatten().tolist()

######### ILUO #########
def getMatrizILUO(archivo):
    """
    Obtiene la matriz ILUO (trabajadores y puestos) desde la hoja "ILUO" en las columnas C a R.
    """
    # Leer la hoja "ILUO" del archivo de Excel, especificando las columnas y filas necesarias
    df_ILUO = pd.read_excel(archivo, sheet_name='ILUO', usecols="C:R")

    # Convertir todos los valores a integer
    df_ILUO = df_ILUO.fillna(0).astype(int)

    # Convertir el DataFrame en una matriz (lista de listas)
    return df_ILUO.values.tolist()


######### Prioridades #########
def getMatrizPrioridades(archivo):
    """
    Lee la matriz de prioridades desde la hoja "Prioridades", ajustando los valores cero a tres.
    """
    # Leer la hoja "Prioridades" del archivo de Excel, especificando las columnas y filas necesarias
    df_Prioridades = pd.read_excel(archivo, sheet_name='Prioridades', usecols="B:Q")

    # Convertir todos los valores a integer
    df_Prioridades = df_Prioridades.fillna(0).astype(int)

    # Convertir el DataFrame en una matriz (lista de listas)
    matriz = df_Prioridades.values.tolist()

    # Reemplazar los valores 0 a 3, para que la función objetivo no cree indeterminados
    for linea_index in range(len(matriz)):
        matriz[linea_index] = [3 if x == 0 else x for x in matriz[linea_index]]

    return matriz


######### Maq_Prio #########
def getArrayMapPrio(archivo):
    """
    Obtiene la lista de prioridades por máquina desde la hoja "Maq_Prio".
    """
    # Leer solo la columna B de la hoja "Maq_Prio"
    df_Maq_Prio = pd.read_excel(archivo, sheet_name='Maq_Prio', usecols="B")

    # Convertir todos los valores a integer
    df_Maq_Prio = df_Maq_Prio.fillna(0).astype(int)

    # Convertir la columna en una lista (array de una sola columna)
    return df_Maq_Prio.squeeze().tolist()


######### OP_Maq #########
def getArrayOPMaq(archivo):
    """
    Extrae la cantidad de operadores por máquina desde la hoja "OP_Maq", creando listas para celdas con múltiples valores.
    """
    # Leer solo la columna B de la hoja "OP_Maq"
    df_OP_Maq = pd.read_excel(archivo, sheet_name='OP_Maq', usecols="B", dtype=str)

    # Convertir cada celda en una lista o en un número entero según su contenido
    result = []
    for item in df_OP_Maq.squeeze():
        # Si hay múltiples valores en una celda, dividirlos y convertirlos a int
        if ',' in item:
            sublist = [int(x) for x in item.split(',')]
            result.append(sublist)
        else:
            # Convertir celdas de un solo valor a int
            result.append(int(item))
    
    return result

######### MAIN #########

def getTablesInfo(archivo):
    """
    Reúne y valida toda la información de trabajadores, puestos, ILUO, prioridades, y asignaciones.
    """
    trabajadores_por_equipo = getTrabajadoresPorEquipo(archivo)

    array_id_trabajadores = getIdTrabajadores(archivo)
    cantidad_trabajadores = len(array_id_trabajadores)

    array_puestos_de_trabajo = getPuestosDeTrabajo(archivo)
    cantidad_puestos = len(array_puestos_de_trabajo)

    matriz_ILUO = getMatrizILUO(archivo)
    if len(matriz_ILUO) != cantidad_trabajadores or len(matriz_ILUO[0]) != cantidad_puestos:
        print(" ¡¡AVISO!! LAS DIMENSIONES DE LA MATRIZ ILUO NO SON CORRECTAS")
        matriz_ILUO = []

    matriz_Prioridades = getMatrizPrioridades(archivo)
    if len(matriz_Prioridades) != cantidad_trabajadores or len(matriz_Prioridades[0]) != cantidad_puestos:
        print(" ¡¡AVISO!! LAS DIMENSIONES DE LA MATRIZ PRIORIDADES NO SON CORRECTAS")
        matriz_Prioridades = []

    array_Maq_Prio = getArrayMapPrio(archivo)
    if len(array_Maq_Prio) != cantidad_puestos:
        print(" ¡¡AVISO!! LAS DIMENSIONES DEL ARRAY PRIORIDADES DE MAQUINAS NO ES CORRECTO")
        array_Maq_Prio = []

    array_OP_Maq = getArrayOPMaq(archivo)
    if len(array_OP_Maq) != cantidad_puestos:
        print(" ¡¡AVISO!! LAS DIMENSIONES DEL ARRAY CANTIDAD DE TRABAJADORES POR MAQUINAS NO ES CORRECTO")
        array_OP_Maq = []

    return (trabajadores_por_equipo, array_id_trabajadores, cantidad_trabajadores, array_puestos_de_trabajo, cantidad_puestos, matriz_ILUO, matriz_Prioridades, array_Maq_Prio, array_OP_Maq)