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
    def getAttributes(self):
        """
        Imprime los atributos.
        """
        readTables.printTablesInfo(self.trabajadores_por_equipo, 
                                   self.array_id_trabajadores, 
                                   self.cantidad_trabajadores, 
                                   self.array_puestos_de_trabajo, 
                                   self.cantidad_puestos, 
                                   self.matriz_ILUO, 
                                   self.matriz_Prioridades, 
                                   self.array_Maq_Prio, 
                                   self.array_OP_Maq)