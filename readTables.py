import pandas as pd
# Si da error descarga estas dos librearias metiendo estos comando en la terminal:
# pip install pandas
# pip install openpyxl


######### ILUO #########

def getMatrizILUO():

    # Leer la hoja "ILUO" del archivo de Excel, especificando las columnas y filas necesarias
    df_ILUO = pd.read_excel(archivo, sheet_name='ILUO', usecols="C:V", skiprows= 0, nrows=79)

    # Convertir todos los valores a integer
    df_ILUO = df_ILUO.fillna(0).astype(int)

    # Convertir el DataFrame en una matriz (lista de listas)
    return df_ILUO.values.tolist()


######### Prioridades #########

def getMatrizPrioridades():
    # Leer la hoja "ILUO" del archivo de Excel, especificando las columnas y filas necesarias
    df_Prioridades = pd.read_excel(archivo, sheet_name='Prioridades', usecols="B:U", skiprows= 0, nrows=79)

    # Convertir todos los valores a integer
    df_Prioridades = df_Prioridades.fillna(0).astype(int)

    # Convertir el DataFrame en una matriz (lista de listas)
    return df_Prioridades.values.tolist()


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

print(" \n -------- MATRIZ ILUO --------")
matriz_ILUO = getMatrizILUO()
for i in range(len(matriz_ILUO)):
    print(matriz_ILUO[i])

print(" \n -------- MATRIZ PRIORIDADES --------")
matriz_Prioridades = getMatrizPrioridades()
for i in range(len(matriz_Prioridades)):
    print(matriz_Prioridades[i])

print(" \n -------- ARRAY PRIORIDADES DE CADA MAQUINA --------")
array_Maq_Prio = getArrayMapPrio()
print(array_Maq_Prio)

print(" \n -------- ARRAY CANTIDAD DE OPERADORES POR MÁQUINA --------")
array_OP_Maq = getArrayOPMaq()
print(array_OP_Maq)