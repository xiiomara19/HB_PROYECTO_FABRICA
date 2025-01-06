import readTables

class Table:

    #Constructor
    def __init__(self, archivo):
        """
        Initializa los atributos.
        """
        (self.trabajadores_por_equipo, 
         self.array_id_trabajadores, 
         self.cantidad_trabajadores, 
         self.array_puestos_de_trabajo, 
         self.cantidad_puestos, 
         self.matriz_ILUO, 
         self.matriz_Prioridades, 
         self.array_Maq_Prio, 
         self.array_OP_Maq) = readTables.getTablesInfo(archivo)
        

    #Métodos
    def printAttributes(self):
        """
        Imprime los datos obtenidos del archivo Excel, incluyendo trabajadores, puestos, matrices ILUO y prioridades.
        """
        print(" \n -------- DICCIONARIO TRABAJADORES POR CADA EQUIPO --------")
        print(self.trabajadores_por_equipo)

        print(" \n -------- ARRAY Ids TRABAJADORES --------")
        print("Cantidad de trabajadores = ", self.cantidad_trabajadores)
        print(self.array_id_trabajadores)

        print(" \n -------- ARRAY PUESTO DE TRABAJO --------")
        print("Cantidad de puestos = ", self.cantidad_puestos)
        print(self.array_puestos_de_trabajo)

        print(" \n -------- MATRIZ ILUO --------")
        if not self.matriz_ILUO:
            print(" ¡¡AVISO!! LAS DIMENSIONES DE LA MATRIZ ILUO NO SON CORRECTAS")
        else:
            for row in self.matriz_ILUO:
                print(row)

        print(" \n -------- MATRIZ PRIORIDADES --------")
        if not self.matriz_Prioridades:
            print(" ¡¡AVISO!! LAS DIMENSIONES DE LA MATRIZ PRIORIDADES NO SON CORRECTAS")
        else:
            for row in self.matriz_Prioridades:
                print(row)

        print(" \n -------- ARRAY PRIORIDADES DE CADA MAQUINA --------")
        if not self.array_Maq_Prio:
            print(" ¡¡AVISO!! LAS DIMENSIONES DEL ARRAY PRIORIDADES DE MAQUINAS NO ES CORRECTO")
        else:
            print(self.array_Maq_Prio)

        print(" \n -------- ARRAY CANTIDAD DE OPERADORES POR MÁQUINA --------")
        if not self.array_OP_Maq:
            print(" ¡¡AVISO!! LAS DIMENSIONES DEL ARRAY CANTIDAD DE TRABAJADORES POR MAQUINAS NO ES CORRECTO")
        else:
            print(self.array_OP_Maq)
        
    def asignar_valores_por_equipo(self, equipo_usuario):
        """
        Crear un resultado local
        """
        # Crear una lista de valores de -1 (inicialmente para todos los trabajadores)
        array_trabajadores_disponibles = [False] * self.cantidad_trabajadores 

        trabajadores_equipo_usuario = self.trabajadores_por_equipo[equipo_usuario]

        for index, id_trabajador in enumerate(self.array_id_trabajadores):
            if id_trabajador in trabajadores_equipo_usuario:
                array_trabajadores_disponibles[index] = True

        return array_trabajadores_disponibles