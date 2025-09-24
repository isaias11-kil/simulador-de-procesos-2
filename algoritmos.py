 # algoritmos.py
from typing import List, Dict, Tuple
from procesos import Proceso
import heapq

class AlgoritmoPlanificacion:
    """Clase base para todos los algoritmos de planificación"""
    
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion
        self.metricas = {}
        self.tiempo_actual = 0
    
    def ejecutar(self, procesos: List[Proceso]) -> List[Dict]:
        """Método abstracto que debe ser implementado por cada algoritmo"""
        raise NotImplementedError("Este método debe ser implementado por las subclases")
    
    def calcular_metricas(self, procesos: List[Proceso]) -> Dict:
        """Calcula métricas comunes para todos los algoritmos"""
        if not procesos:
            return {}
        
        tiempos_espera = []
        tiempos_respuesta = []
        tiempos_retorno = []
        
        for proceso in procesos:
            if (proceso.tiempo_finalizacion is not None and 
                proceso.tiempo_respuesta is not None):
                
                turnaround = proceso.tiempo_finalizacion - proceso.instante_llegada
                tiempo_retorno = turnaround
                tiempo_espera = proceso.tiempo_espera
                tiempo_respuesta = proceso.tiempo_respuesta
                
                tiempos_retorno.append(tiempo_retorno)
                tiempos_espera.append(tiempo_espera)
                tiempos_respuesta.append(tiempo_respuesta)
        
        metricas = {
            'throughput': len([p for p in procesos if p.tiempo_finalizacion is not None]),
            'tiempo_retorno_promedio': sum(tiempos_retorno) / len(tiempos_retorno) if tiempos_retorno else 0,
            'tiempo_espera_promedio': sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0,
            'tiempo_respuesta_promedio': sum(tiempos_respuesta) / len(tiempos_respuesta) if tiempos_respuesta else 0,
            'uso_cpu': (self.tiempo_actual - sum(tiempos_espera)) / self.tiempo_actual if self.tiempo_actual > 0 else 0
        }
        
        return metricas

class FCFS(AlgoritmoPlanificacion):
    """First Come First Served (FIFO) - No apropiativo"""
    
    def __init__(self):
        super().__init__("FCFS", "First Come First Served - No apropiativo")
    
    def ejecutar(self, procesos: List[Proceso]) -> List[Dict]:
        """Ejecuta el algoritmo FCFS"""
        self.tiempo_actual = 0
        eventos = []
        
        # Ordenar procesos por tiempo de llegada
        procesos_ordenados = sorted(procesos, key=lambda x: x.instante_llegada)
        
        for proceso in procesos_ordenados:
            # Esperar hasta que el proceso llegue
            if self.tiempo_actual < proceso.instante_llegada:
                self.tiempo_actual = proceso.instante_llegada
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': f"Proceso {proceso.nombre} llega al sistema"
                })
            
            # Tiempo de respuesta (primera vez que se ejecuta)
            if not proceso.ejecutado:
                proceso.tiempo_respuesta = self.tiempo_actual - proceso.instante_llegada
                proceso.ejecutado = True
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': f"Inicia ejecución de {proceso.nombre} (PID: {proceso.pid})"
                })
            
            # Ejecutar el proceso completo
            inicio_ejecucion = self.tiempo_actual
            self.tiempo_actual += proceso.tiempo_cpu
            proceso.tiempo_restante = 0
            proceso.tiempo_finalizacion = self.tiempo_actual
            
            # Calcular tiempo de espera
            proceso.tiempo_espera = inicio_ejecucion - proceso.instante_llegada
            
            eventos.append({
                'tiempo': self.tiempo_actual,
                'evento': f"Finaliza {proceso.nombre} | Espera: {proceso.tiempo_espera}"
            })
        
        self.metricas = self.calcular_metricas(procesos)
        return eventos

class SJF(AlgoritmoPlanificacion):
    """Shortest Job First (No apropiativo)"""
    
    def __init__(self):
        super().__init__("SJF", "Shortest Job First - No apropiativo")
    
    def ejecutar(self, procesos: List[Proceso]) -> List[Dict]:
        """Ejecuta el algoritmo SJF no apropiativo"""
        self.tiempo_actual = 0
        eventos = []
        completados = []
        cola_espera = []
        
        # Ordenar procesos por llegada inicialmente
        procesos_restantes = sorted(procesos, key=lambda x: x.instante_llegada)
        
        while len(completados) < len(procesos):
            # Agregar procesos que han llegado a la cola de espera
            llegados = [p for p in procesos_restantes 
                       if p.instante_llegada <= self.tiempo_actual and p not in completados]
            
            for p in llegados:
                if p not in cola_espera:
                    cola_espera.append(p)
                    eventos.append({
                        'tiempo': self.tiempo_actual,
                        'evento': f"{p.nombre} llega a cola de espera"
                    })
            
            if cola_espera:
                # Seleccionar el proceso con menor tiempo de CPU
                cola_espera.sort(key=lambda x: x.tiempo_cpu)
                proceso_actual = cola_espera.pop(0)
                
                # Tiempo de respuesta
                if not proceso_actual.ejecutado:
                    proceso_actual.tiempo_respuesta = self.tiempo_actual - proceso_actual.instante_llegada
                    proceso_actual.ejecutado = True
                
                inicio_ejecucion = self.tiempo_actual
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': f"SJF selecciona {proceso_actual.nombre} (CPU: {proceso_actual.tiempo_cpu})"
                })
                
                # Ejecutar proceso completo
                self.tiempo_actual += proceso_actual.tiempo_cpu
                proceso_actual.tiempo_restante = 0
                proceso_actual.tiempo_finalizacion = self.tiempo_actual
                proceso_actual.tiempo_espera = inicio_ejecucion - proceso_actual.instante_llegada
                
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': f"Finaliza {proceso_actual.nombre} | Espera: {proceso_actual.tiempo_espera}"
                })
                
                completados.append(proceso_actual)
                procesos_restantes.remove(proceso_actual)
            else:
                # No hay procesos listos, avanzar tiempo
                self.tiempo_actual += 1
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': "CPU idle - Esperando procesos"
                })
        
        self.metricas = self.calcular_metricas(procesos)
        return eventos

class SRTF(AlgoritmoPlanificacion):
    """Shortest Remaining Time First (Apropiativo)"""
    
    def __init__(self):
        super().__init__("SRTF", "Shortest Remaining Time First - Apropiativo")
    
    def ejecutar(self, procesos: List[Proceso]) -> List[Dict]:
        """Ejecuta el algoritmo SRTF"""
        self.tiempo_actual = 0
        eventos = []
        
        # Inicializar procesos
        for p in procesos:
            p.tiempo_restante = p.tiempo_cpu
            p.ejecutado = False
        
        completados = []
        proceso_actual = None
        tiempo_inicio_ejecucion = 0
        
        while len(completados) < len(procesos):
            # Verificar si llegan nuevos procesos
            nuevos = [p for p in procesos 
                     if p.instante_llegada == self.tiempo_actual and p not in completados]
            
            for p in nuevos:
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': f"{p.nombre} llega al sistema"
                })
            
            # Obtener procesos listos para ejecutar
            procesos_listos = [p for p in procesos 
                             if p.instante_llegada <= self.tiempo_actual 
                             and p.tiempo_restante > 0 
                             and p not in completados]
            
            if procesos_listos:
                # Seleccionar proceso con menor tiempo restante
                procesos_listos.sort(key=lambda x: x.tiempo_restante)
                nuevo_proceso = procesos_listos[0]
                
                # Verificar si hay cambio de proceso
                if proceso_actual != nuevo_proceso:
                    if proceso_actual is not None:
                        # Registrar tiempo de ejecución del proceso anterior
                        tiempo_ejecutado = self.tiempo_actual - tiempo_inicio_ejecucion
                        proceso_actual.tiempo_restante -= tiempo_ejecutado
                        
                        if proceso_actual.tiempo_restante <= 0:
                            proceso_actual.tiempo_finalizacion = self.tiempo_actual
                            completados.append(proceso_actual)
                            eventos.append({
                                'tiempo': self.tiempo_actual,
                                'evento': f"Finaliza {proceso_actual.nombre}"
                            })
                    
                    proceso_actual = nuevo_proceso
                    tiempo_inicio_ejecucion = self.tiempo_actual
                    
                    if not proceso_actual.ejecutado:
                        proceso_actual.tiempo_respuesta = self.tiempo_actual - proceso_actual.instante_llegada
                        proceso_actual.ejecutado = True
                    
                    eventos.append({
                        'tiempo': self.tiempo_actual,
                        'evento': f"SRTF cambia a {proceso_actual.nombre} (Restante: {proceso_actual.tiempo_restante})"
                    })
                
                # Ejecutar una unidad de tiempo
                self.tiempo_actual += 1
                
            else:
                # CPU idle
                proceso_actual = None
                self.tiempo_actual += 1
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': "CPU idle"
                })
        
        # Calcular tiempos de espera
        for p in procesos:
            p.tiempo_espera = p.tiempo_finalizacion - p.instante_llegada - p.tiempo_cpu
        
        self.metricas = self.calcular_metricas(procesos)
        return eventos

class RoundRobin(AlgoritmoPlanificacion):
    """Round Robin con quantum configurable"""
    
    def __init__(self, quantum: int = 2):
        super().__init__("Round Robin", f"Round Robin con quantum={quantum}")
        self.quantum = quantum
    
    def ejecutar(self, procesos: List[Proceso]) -> List[Dict]:
        """Ejecuta el algoritmo Round Robin"""
        self.tiempo_actual = 0
        eventos = []
        
        # Inicializar procesos
        for p in procesos:
            p.tiempo_restante = p.tiempo_cpu
            p.ejecutado = False
        
        # Crear cola Round Robin
        cola = []
        completados = []
        
        # Ordenar procesos por llegada
        procesos_por_llegada = sorted(procesos, key=lambda x: x.instante_llegada)
        indice_proximo = 0
        
        while len(completados) < len(procesos):
            # Agregar procesos que han llegado
            while (indice_proximo < len(procesos_por_llegada) and 
                   procesos_por_llegada[indice_proximo].instante_llegada <= self.tiempo_actual):
                proceso = procesos_por_llegada[indice_proximo]
                cola.append(proceso)
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': f"{proceso.nombre} se agrega a cola RR"
                })
                indice_proximo += 1
            
            if cola:
                proceso_actual = cola.pop(0)
                
                # Tiempo de respuesta si es primera ejecución
                if not proceso_actual.ejecutado:
                    proceso_actual.tiempo_respuesta = self.tiempo_actual - proceso_actual.instante_llegada
                    proceso_actual.ejecutado = True
                    eventos.append({
                        'tiempo': self.tiempo_actual,
                        'evento': f"RR inicia {proceso_actual.nombre} (Quantum: {self.quantum})"
                    })
                
                # Ejecutar por quantum o hasta completar
                tiempo_ejecucion = min(self.quantum, proceso_actual.tiempo_restante)
                inicio_bloque = self.tiempo_actual
                
                for i in range(tiempo_ejecucion):
                    self.tiempo_actual += 1
                    proceso_actual.tiempo_restante -= 1
                    
                    # Verificar si llegan nuevos procesos durante la ejecución
                    while (indice_proximo < len(procesos_por_llegada) and 
                           procesos_por_llegada[indice_proximo].instante_llegada <= self.tiempo_actual):
                        nuevo = procesos_por_llegada[indice_proximo]
                        cola.append(nuevo)
                        eventos.append({
                            'tiempo': self.tiempo_actual,
                            'evento': f"{nuevo.nombre} llega durante ejecución"
                        })
                        indice_proximo += 1
                
                if proceso_actual.tiempo_restante > 0:
                    # El proceso no ha terminado, volver a la cola
                    cola.append(proceso_actual)
                    eventos.append({
                        'tiempo': self.tiempo_actual,
                        'evento': f"{proceso_actual.nombre} vuelve a cola ({proceso_actual.tiempo_restante} restante)"
                    })
                else:
                    # Proceso completado
                    proceso_actual.tiempo_finalizacion = self.tiempo_actual
                    completados.append(proceso_actual)
                    proceso_actual.tiempo_espera = (proceso_actual.tiempo_finalizacion - 
                                                  proceso_actual.instante_llegada - 
                                                  proceso_actual.tiempo_cpu)
                    eventos.append({
                        'tiempo': self.tiempo_actual,
                        'evento': f"✅ {proceso_actual.nombre} completado | Espera: {proceso_actual.tiempo_espera}"
                    })
            else:
                # CPU idle
                self.tiempo_actual += 1
                eventos.append({
                    'tiempo': self.tiempo_actual,
                    'evento': "CPU idle - Cola vacía"
                })
        
        self.metricas = self.calcular_metricas(procesos)
        return eventos

class Prioridades(AlgoritmoPlanificacion):
    """Planificación por prioridades (menor número = mayor prioridad)"""
    
    def __init__(self, apropiativo: bool = True):
        nombre = "Prioridades Apropiativo" if apropiativo else "Prioridades No Apropiativo"
        super().__init__("Prioridades", nombre)
        self.apropiativo = apropiativo
    
    def ejecutar(self, procesos: List[Proceso]) -> List[Dict]:
        """Ejecuta planificación por prioridades"""
        # Para simplificar, asumimos que cada proceso tiene un atributo 'prioridad'
        # Si no existe, usamos tiempo de CPU como prioridad (menor CPU = mayor prioridad)
        
        eventos = [{
            'tiempo': 0,
            'evento': "Algoritmo de Prioridades no implementado completamente"
        }]
        
        self.metricas = self.calcular_metricas(procesos)
        return eventos

# Fábrica de algoritmos
class FabricaAlgoritmos:
    """Fábrica para crear instancias de algoritmos"""
    
    @staticmethod
    def crear_algoritmo(nombre: str, **kwargs) -> AlgoritmoPlanificacion:
        algoritmos = {
            "FCFS": FCFS,
            "SJF": SJF,
            "SRTF": SRTF,
            "Round Robin": RoundRobin,
            "Prioridades": Prioridades
        }
        
        if nombre not in algoritmos:
            raise ValueError(f"Algoritmo '{nombre}' no soportado")
        
        if nombre == "Round Robin":
            quantum = kwargs.get('quantum', 2)
            return RoundRobin(quantum)
        elif nombre == "Prioridades":
            apropiativo = kwargs.get('apropiativo', True)
            return Prioridades(apropiativo)
        else:
            return algoritmos[nombre]()
    
    @staticmethod
    def obtener_algoritmos_disponibles() -> List[str]:
        return ["FCFS", "SJF", "SRTF", "Round Robin", "Prioridades"]
    
    @staticmethod
    def obtener_descripcion(algoritmo: str) -> str:
        descripciones = {
            "FCFS": "First Come First Served - No apropiativo",
            "SJF": "Shortest Job First - No apropiativo",
            "SRTF": "Shortest Remaining Time First - Apropiativo",
            "Round Robin": "Round Robin - Apropiativo con quantum",
            "Prioridades": "Planificación por prioridades"
        }
        return descripciones.get(algoritmo, "Descripción no disponible")

# Función de utilidad para análisis comparativo
def analizar_comparativo(procesos: List[Proceso]) -> Dict:
    """Ejecuta todos los algoritmos y compara métricas"""
    resultados = {}
    fabrica = FabricaAlgoritmos()
    
    for nombre_algoritmo in fabrica.obtener_algoritmos_disponibles():
        try:
            # Crear copia de procesos para cada algoritmo
            procesos_copia = []
            for p in procesos:
                nuevo_proceso = Proceso(p.nombre, p.tiempo_cpu, p.instante_llegada, p.quantum)
                procesos_copia.append(nuevo_proceso)
            
            algoritmo = fabrica.crear_algoritmo(nombre_algoritmo)
            eventos = algoritmo.ejecutar(procesos_copia)
            
            resultados[nombre_algoritmo] = {
                'metricas': algoritmo.metricas,
                'eventos': eventos,
                'tiempo_total': algoritmo.tiempo_actual
            }
            
        except Exception as e:
            resultados[nombre_algoritmo] = {
                'error': str(e),
                'metricas': {},
                'eventos': []
            }
    
    return resultados

if __name__ == "__main__":
    # Ejemplo de uso
    procesos_ejemplo = [
        Proceso("P1", 5, 0),
        Proceso("P2", 3, 1),
        Proceso("P3", 8, 2)
    ]
    
    # Probar FCFS
    fcfs = FCFS()
    eventos = fcfs.ejecutar(procesos_ejemplo)
    
    print("=== FCFS ===")
    for evento in eventos:
        print(f"T{evento['tiempo']}: {evento['evento']}")
    
    print("\nMétricas:", fcfs.metricas)

