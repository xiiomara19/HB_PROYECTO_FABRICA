import pandas as pd
# Si da error descarga estas dos librearias metiendo estos comando en la terminal:
# pip install pandas
# pip install openpyxl

######### IDs DE TRABAJADORES #########
def getIdTrabajadores():

    # Leer solo la columna B de la hoja "ILUO"
    df_id_trabajadores = pd.read_excel(archivo, sheet_name='ILUO', usecols="B", skiprows= 0, nrows=79)

    # Convertir todos los valores a integer
    df_id_trabajadores = df_id_trabajadores.fillna(0).astype(int)

    # Convertir la columna en una lista (array de una sola columna)
    return df_id_trabajadores.squeeze().tolist()

######### PUESTOS DE TRABAJO #########
def getPuestosDeTrabajo():

    # Leer solo la primera fila de las columnas C a S en la hoja "ILUO"
    df_puestos_trabajo = pd.read_excel(archivo, sheet_name='ILUO', usecols="C:R", nrows=1, header=None)

    # Convertir todos los valores a tipo string
    df_puestos_trabajo = df_puestos_trabajo.astype(str)

    # Convertir el DataFrame en una lista (array)
    return df_puestos_trabajo.values.flatten().tolist()

######### ILUO #########

def getMatrizILUO():

    # Leer la hoja "ILUO" del archivo de Excel, especificando las columnas y filas necesarias
    df_ILUO = pd.read_excel(archivo, sheet_name='ILUO', usecols="C:R", skiprows= 0, nrows=79)

    # Convertir todos los valores a integer
    df_ILUO = df_ILUO.fillna(0).astype(int)

    # Convertir el DataFrame en una matriz (lista de listas)
    return df_ILUO.values.tolist()


######### Prioridades #########

def getMatrizPrioridades():
    # Leer la hoja "Prioridades" del archivo de Excel, especificando las columnas y filas necesarias
    df_Prioridades = pd.read_excel(archivo, sheet_name='Prioridades', usecols="B:Q", nrows=79)

    # Convertir todos los valores a integer
    df_Prioridades = df_Prioridades.fillna(0).astype(int)

    # Convertir el DataFrame en una matriz (lista de listas)
    matriz = df_Prioridades.values.tolist()

    # Reemplazar los valores 0 a 3, para que la función objetivo no cree indeterminados
    for linea_index in range(len(matriz)):
        matriz[linea_index] = [3 if x == 0 else x for x in matriz[linea_index]]

    return matriz


######### Maq_Prio #########

def getArrayMapPrio():
        
    # Leer solo la columna B de la hoja "Maq_Prio"
    df_Maq_Prio = pd.read_excel(archivo, sheet_name='Maq_Prio', usecols="B")

    # Convertir todos los valores a integer
    df_Maq_Prio = df_Maq_Prio.fillna(0).astype(int)

    # Convertir la columna en una lista (array de una sola columna)
    return df_Maq_Prio.squeeze().tolist()


######### OP_Maq #########

def getArrayOPMaq():

    # Leer solo la columna B de la hoja "OP_Maq"
    df_OP_Maq = pd.read_excel(archivo, sheet_name='OP_Maq', usecols="B")

    # Convertir todos los valores a integer
    # df_OP_Maq = df_OP_Maq.fillna(0).astype(int)

    # Convertir la columna en una lista (array de una sola columna)
    return df_OP_Maq.squeeze().tolist()


######### MAIN #########

# Ruta del archivo de Excel
archivo = 'DATOS turnos HB compartir.xlsm'


print(" \n -------- ARRAY Ids TRABAJADORES --------")
array_id_trabajadores = getIdTrabajadores()
cantidad_trabajadores = len(array_id_trabajadores)
print("Cantidad de trabajadores = ", cantidad_trabajadores)
print(array_id_trabajadores)

print(" \n -------- ARRAY PUESTO DE TRABAJO --------")
array_puestos_de_trabajo = getPuestosDeTrabajo()
cantidad_puestos = len(array_puestos_de_trabajo)
print("Cantidad de puestos = ", cantidad_puestos)
print(array_puestos_de_trabajo)

print(" \n -------- MATRIZ ILUO --------")
matriz_ILUO = getMatrizILUO()
if len(matriz_ILUO) != cantidad_trabajadores or len(matriz_ILUO[0]) != cantidad_puestos:
    print(" ¡¡AVISO!! LAS DIMENSIONES DE LA MATRIZ ILUO NO SON CORRECTAS")
else:
    for i in range(len(matriz_ILUO)):
        print(matriz_ILUO[i])

print(" \n -------- MATRIZ PRIORIDADES --------")
matriz_Prioridades = getMatrizPrioridades()
if len(matriz_Prioridades) != cantidad_trabajadores or len(matriz_Prioridades[0]) != cantidad_puestos:
    print(" ¡¡AVISO!! LAS DIMENSIONES DE LA MATRIZ PRIORIDADES NO SON CORRECTAS")
else:
    for i in range(len(matriz_Prioridades)):
        print(matriz_Prioridades[i])

print(" \n -------- ARRAY PRIORIDADES DE CADA MAQUINA --------")
array_Maq_Prio = getArrayMapPrio()
if len(array_Maq_Prio) != cantidad_puestos:
    print(" ¡¡AVISO!! LAS DIMENSIONES DEL ARRAY PRIORIDADES DE MAQUINAS NO ES CORRECTO")
else:
    print(array_Maq_Prio)

print(" \n -------- ARRAY CANTIDAD DE OPERADORES POR MÁQUINA --------")
array_OP_Maq = getArrayOPMaq()
if len(array_OP_Maq) != cantidad_puestos:
    print(" ¡¡AVISO!! LAS DIMENSIONES DEL ARRAY CANTIDAD DE TRABAJADORES POR MAQUINAS NO ES CORRECTO")
else:
    print(array_OP_Maq)
