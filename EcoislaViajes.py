class viaje: 
    def __init__(self, horario):
        self.horario=horario
        self.matriz_asientos= self.iniciar_matriz()
        self.ventas_totales=0
        self.recaudacion=0.0

    def iniciar_matriz(self):
        return  [[0]* 5 for _ in range(5)]
         
##class Asiento: 
    ## def __init__(self,asiento, estado):
    ##   self.asiento=asiento
    ##   self.estado=estado
## CLASE PARA IMPLEMENTAR LUEGO 

##class Reservas: 

##CLASE PARA IMPLEMENTAR LUEGO 

class embarcacion: 
    def __init__(self, nombre):
        self.nombre=nombre
    
        self.viajes=self.crear_viaje()

        self.ganancia_total= 0.0

    def crear_viaje(self):
        horarios = [ "Mañana", "Tarde", "Noche"]
        viajes_dict={}

        for h in horarios: 
            viajes_dict[h] = viaje(h)

        return viajes_dict

SistemaEcoviajes = [
    embarcacion("Esmeralda"),
    embarcacion("Goleta"),
    embarcacion("Covadonga")
]

print("--- RESERVAS DE ECOVIAJES ---")

embarcacion_1 = SistemaEcoviajes[0] 
print(f"Embarcación Cargada: {embarcacion_1.nombre}")

viaje_manana = embarcacion_1.viajes["Mañana"]
print(f"Horario del Viaje: {viaje_manana.horario}")
print(f"Ventas iniciales: {viaje_manana.ventas_totales}")

print("\nMatriz de Asientos (Mañana de Esmeralda):")
for fila in viaje_manana.matriz_asientos:
    print(fila)

