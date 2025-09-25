
class Proceso:
    _ultimo_pid = 0 

    def __init__(self, nombre, tiempo_cpu, instante_llegada, quantum=None):
       
        Proceso._ultimo_pid += 1
        self.pid = Proceso._ultimo_pid
        
     
        self.nombre = nombre
        self.tiempo_cpu = tiempo_cpu
        self.instante_llegada = instante_llegada
        self.quantum = quantum

       
        self.tiempo_restante = tiempo_cpu
        self.tiempo_finalizacion = None
        self.tiempo_espera = 0
        self.tiempo_respuesta = None
        self.ejecutado = False

    def __repr__(self):
            return (f"Proceso(pid={self.pid}, nombre='{self.nombre}', "
            f"tiempo_cpu={self.tiempo_cpu}, llegada={self.instante_llegada}, "
            f"quantum={self.quantum})")

def crear_proceso(nombre, tiempo_cpu, instante_llegada, quantum=None):
    if not nombre or not isinstance(nombre, str):
        raise ValueError("El nombre del proceso no puede estar vacío.")
    if not isinstance(tiempo_cpu, int) or tiempo_cpu <= 0:
        raise ValueError("El tiempo de CPU debe ser un entero positivo.")
    if not isinstance(instante_llegada, int) or instante_llegada < 0:
        raise ValueError("El instante de llegada debe ser un entero mayor o igual a 0.")
    if quantum is not None and (not isinstance(quantum, int) or quantum <= 0):
        raise ValueError("El quantum debe ser un entero positivo (si aplica).")
    
    return Proceso(nombre, tiempo_cpu, instante_llegada, quantum)


