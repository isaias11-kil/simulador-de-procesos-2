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
        super().__init__("FCFS", "First Come First Served")
    
    def ejecutar(self, procesos: List[Proceso], on_proceso_finalizado=None) -> List[Dict]:
        eventos = []
        procesos_ordenados = sorted(procesos, key=lambda x: x.instante_llegada)
        tiempo_actual = 0

        for proceso in procesos_ordenados:
            if tiempo_actual < proceso.instante_llegada:
                tiempo_actual = proceso.instante_llegada
            proceso.tiempo_espera = tiempo_actual - proceso.instante_llegada
            proceso.tiempo_respuesta = proceso.tiempo_espera
            tiempo_actual += proceso.tiempo_cpu
            proceso.tiempo_finalizacion = tiempo_actual
            proceso.ejecutado = True

            evento = {
                "pid": proceso.pid,
                "nombre": proceso.nombre,
                "inicio": tiempo_actual - proceso.tiempo_cpu,
                "fin": proceso.tiempo_finalizacion,
                "algoritmo": self.nombre
            }
            eventos.append(evento)

            if on_proceso_finalizado:
                info = (f"PID {proceso.pid} - {proceso.nombre} "
                        f"finalizado | Algoritmo: {self.nombre} | "
                        f"Llegada: {proceso.instante_llegada} | "
                        f"CPU: {proceso.tiempo_cpu} | "
                        f"Finalización: {proceso.tiempo_finalizacion}")
                on_proceso_finalizado(info)

        self.metricas = self.calcular_metricas(procesos)
        return eventos

class SJF(AlgoritmoPlanificacion):
    """Shortest Job First (No apropiativo)"""
    
    def __init__(self):
        super().__init__("SJF", "Shortest Job First")
    
    def ejecutar(self, procesos: List[Proceso], on_proceso_finalizado=None) -> List[Dict]:
        eventos = []
        procesos_ordenados = sorted(procesos, key=lambda x: (x.instante_llegada, x.tiempo_cpu))
        tiempo_actual = 0
        cola = procesos_ordenados.copy()
        ejecutados = []

        while cola:
            disponibles = [p for p in cola if p.instante_llegada <= tiempo_actual]
            if not disponibles:
                tiempo_actual = cola[0].instante_llegada
                disponibles = [cola[0]]
            proceso = min(disponibles, key=lambda x: x.tiempo_cpu)
            cola.remove(proceso)
            proceso.tiempo_espera = max(0, tiempo_actual - proceso.instante_llegada)
            proceso.tiempo_respuesta = proceso.tiempo_espera
            tiempo_actual += proceso.tiempo_cpu
            proceso.tiempo_finalizacion = tiempo_actual
            proceso.ejecutado = True
            ejecutados.append(proceso)

            evento = {
                "pid": proceso.pid,
                "nombre": proceso.nombre,
                "inicio": tiempo_actual - proceso.tiempo_cpu,
                "fin": proceso.tiempo_finalizacion,
                "algoritmo": self.nombre
            }
            eventos.append(evento)

            if on_proceso_finalizado:
                info = (f"PID {proceso.pid} - {proceso.nombre} "
                        f"finalizado | Algoritmo: {self.nombre} | "
                        f"Llegada: {proceso.instante_llegada} | "
                        f"CPU: {proceso.tiempo_cpu} | "
                        f"Finalización: {proceso.tiempo_finalizacion}")
                on_proceso_finalizado(info)

        self.metricas = self.calcular_metricas(ejecutados)
        return eventos

class SRTF(AlgoritmoPlanificacion):
    """Shortest Remaining Time First (Apropiativo)"""
    
    def __init__(self):
        super().__init__("SRTF", "Shortest Remaining Time First")
    
    def ejecutar(self, procesos: List[Proceso], on_proceso_finalizado=None) -> List[Dict]:
        eventos = []
        procesos_copia = [Proceso(p.nombre, p.tiempo_cpu, p.instante_llegada) for p in procesos]
        tiempo_actual = 0
        completados = 0
        n = len(procesos_copia)
        while completados < n:
            disponibles = [p for p in procesos_copia if p.instante_llegada <= tiempo_actual and p.tiempo_restante > 0]
            if disponibles:
                proceso = min(disponibles, key=lambda x: x.tiempo_restante)
                if proceso.tiempo_respuesta is None:
                    proceso.tiempo_respuesta = tiempo_actual - proceso.instante_llegada
                proceso.tiempo_restante -= 1
                tiempo_actual += 1
                if proceso.tiempo_restante == 0:
                    proceso.tiempo_finalizacion = tiempo_actual
                    proceso.tiempo_espera = proceso.tiempo_finalizacion - proceso.instante_llegada - proceso.tiempo_cpu
                    proceso.ejecutado = True
                    completados += 1

                    evento = {
                        "pid": proceso.pid,
                        "nombre": proceso.nombre,
                        "inicio": proceso.instante_llegada,
                        "fin": proceso.tiempo_finalizacion,
                        "algoritmo": self.nombre
                    }
                    eventos.append(evento)

                    if on_proceso_finalizado:
                        info = (f"PID {proceso.pid} - {proceso.nombre} "
                                f"finalizado | Algoritmo: {self.nombre} | "
                                f"Llegada: {proceso.instante_llegada} | "
                                f"CPU: {proceso.tiempo_cpu} | "
                                f"Finalización: {proceso.tiempo_finalizacion}")
                        on_proceso_finalizado(info)
            else:
                tiempo_actual += 1

        self.metricas = self.calcular_metricas(procesos_copia)
        return eventos

class RoundRobin(AlgoritmoPlanificacion):
    """Round Robin con quantum configurable"""
    
    def __init__(self, quantum: int = 2):
        super().__init__("Round Robin", f"Quantum={quantum}")
        self.quantum = quantum
    
    def ejecutar(self, procesos: List[Proceso], on_proceso_finalizado=None) -> List[Dict]:
        eventos = []
        procesos_copia = [Proceso(p.nombre, p.tiempo_cpu, p.instante_llegada, self.quantum) for p in procesos]
        tiempo_actual = 0
        cola = []
        completados = 0
        n = len(procesos_copia)
        llegada_idx = 0

        while completados < n:
            while llegada_idx < n and procesos_copia[llegada_idx].instante_llegada <= tiempo_actual:
                cola.append(procesos_copia[llegada_idx])
                llegada_idx += 1
            if cola:
                proceso = cola.pop(0)
                if proceso.tiempo_respuesta is None:
                    proceso.tiempo_respuesta = tiempo_actual - proceso.instante_llegada
                ejecucion = min(self.quantum, proceso.tiempo_restante)
                proceso.tiempo_restante -= ejecucion
                tiempo_actual += ejecucion
                while llegada_idx < n and procesos_copia[llegada_idx].instante_llegada <= tiempo_actual:
                    cola.append(procesos_copia[llegada_idx])
                    llegada_idx += 1
                if proceso.tiempo_restante == 0:
                    proceso.tiempo_finalizacion = tiempo_actual
                    proceso.tiempo_espera = proceso.tiempo_finalizacion - proceso.instante_llegada - proceso.tiempo_cpu
                    proceso.ejecutado = True
                    completados += 1

                    evento = {
                        "pid": proceso.pid,
                        "nombre": proceso.nombre,
                        "inicio": proceso.instante_llegada,
                        "fin": proceso.tiempo_finalizacion,
                        "algoritmo": self.nombre
                    }
                    eventos.append(evento)

                    if on_proceso_finalizado:
                        info = (f"PID {proceso.pid} - {proceso.nombre} "
                                f"finalizado | Algoritmo: {self.nombre} | "
                                f"Llegada: {proceso.instante_llegada} | "
                                f"CPU: {proceso.tiempo_cpu} | "
                                f"Finalización: {proceso.tiempo_finalizacion}")
                        on_proceso_finalizado(info)
                else:
                    cola.append(proceso)
            else:
                tiempo_actual += 1

        self.metricas = self.calcular_metricas(procesos_copia)
        return eventos



class FabricaAlgoritmos:
    """Fábrica para crear instancias de algoritmos"""
    
    @staticmethod
    def crear_algoritmo(nombre: str, **kwargs) -> AlgoritmoPlanificacion:
        algoritmos = {
            "FCFS": FCFS,
            "SJF": SJF,
            "SRTF": SRTF,
            "Round Robin": RoundRobin
            
        }
        
        if nombre not in algoritmos:
            raise ValueError(f"Algoritmo '{nombre}' no soportado")
        
        if nombre == "Round Robin":
            quantum = kwargs.get('quantum', 2)
            return RoundRobin(quantum)
        
        else:
            return algoritmos[nombre]()
    
    @staticmethod
    def obtener_algoritmos_disponibles() -> List[str]:
        return ["FCFS", "SJF", "SRTF", "Round Robin"]
    
    @staticmethod
    def obtener_descripcion(algoritmo: str) -> str:
        descripciones = {
            "FCFS": "First Come First Served - No apropiativo",
            "SJF": "Shortest Job First - No apropiativo",
            "SRTF": "Shortest Remaining Time First - Apropiativo",
            "Round Robin": "Round Robin - Apropiativo con quantum",
            
        }
        return descripciones.get(algoritmo, "Descripción no disponible")


def analizar_comparativo(procesos: List[Proceso]) -> Dict:
    """Ejecuta todos los algoritmos y compara métricas"""
    resultados = {}
    fabrica = FabricaAlgoritmos()
    
    for nombre_algoritmo in fabrica.obtener_algoritmos_disponibles():
        try:
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
   
    procesos_ejemplo = [
        Proceso("P1", 5, 0),
        Proceso("P2", 3, 1),
        Proceso("P3", 8, 2)
    ]
    
 
    fcfs = FCFS()
    eventos = fcfs.ejecutar(procesos_ejemplo)
    
    print("=== FCFS ===")
    for evento in eventos:
        print(f"T{evento['tiempo']}: {evento['evento']}")
    
    print("\nMétricas:", fcfs.metricas)


