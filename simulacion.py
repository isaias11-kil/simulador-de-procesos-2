import time
import tkinter as tk
from collections import deque
from threading import Thread
from typing import List

class MotorSimulacion:
    def __init__(self, text_widget):
        self.cola_procesos = deque()
        self.tiempo = 0
        self.text_widget = text_widget
        self.simulacion_activa = False
        self.velocidad = 1.0

    def agregar_proceso(self, proceso):
        """Agrega un objeto Proceso (de procesos.py) a la cola"""
        self.cola_procesos.append(proceso)

    def mostrar(self, texto):
        """Muestra texto en el widget de forma segura"""
        try:
            self.text_widget.insert(tk.END, texto + "\n")
            self.text_widget.see(tk.END)
            self.text_widget.update_idletasks()
        except Exception as e:
            print(f"Error mostrando texto: {e}")

    def configurar_velocidad(self, velocidad):
        velocidades = {"lenta": 2.0, "normal": 1.0, "rapida": 0.5}
        self.velocidad = velocidades.get(velocidad, 1.0)

    def iniciar(self, algoritmo="FCFS"):
        """Ejecuta la simulación usando objetos Proceso"""
        self.simulacion_activa = True
        self.mostrar("═" * 50)
        self.mostrar(f"🎯 SIMULACIÓN CON CLASE PROCESO - {algoritmo}")
        self.mostrar("═" * 50)

        if algoritmo == "FCFS":
            self._ejecutar_fcfs()
        elif algoritmo == "SJF":
            self._ejecutar_sjf()
        elif algoritmo == "Round Robin":
            self._ejecutar_round_robin()
        else:
            self.mostrar(f"⚠️  Algoritmo {algoritmo} no implementado, usando FCFS")
            self._ejecutar_fcfs()

        self._mostrar_metricas_finales()
        self.mostrar("✅ SIMULACIÓN COMPLETADA")

    def _ejecutar_fcfs(self):
        """First Come First Served con objetos Proceso"""
        procesos_ordenados = sorted(self.cola_procesos, key=lambda x: x.instante_llegada)
        tiempo_actual = 0

        for proceso in procesos_ordenados:
            if not self.simulacion_activa:
                break

            
            if tiempo_actual < proceso.instante_llegada:
                self.mostrar(f"⏳ T{tiempo_actual}: Esperando llegada de procesos...")
                tiempo_actual = proceso.instante_llegada

            
            if not proceso.ejecutado:
                proceso.tiempo_respuesta = tiempo_actual - proceso.instante_llegada
                proceso.ejecutado = True

            self.mostrar(f"🚀 T{tiempo_actual}: Ejecutando {proceso.nombre} (PID: {proceso.pid})")

           
            for i in range(proceso.tiempo_restante):
                if not self.simulacion_activa:
                    break
                
                tiempo_actual += 1
                proceso.tiempo_restante -= 1
                
                self.mostrar(f"   T{tiempo_actual}: {proceso.nombre} [{i+1}/{proceso.tiempo_cpu}]")
                time.sleep(0.5 * self.velocidad)

                if proceso.tiempo_restante == 0:
                    proceso.tiempo_finalizacion = tiempo_actual
                    break

            if self.simulacion_activa:
                tiempo_espera = proceso.tiempo_finalizacion - proceso.instante_llegada - proceso.tiempo_cpu
                proceso.tiempo_espera = max(0, tiempo_espera)
                
                self.mostrar(f"✅ T{tiempo_actual}: {proceso.nombre} completado")
                self.mostrar(f"   📊 Métricas: Espera={proceso.tiempo_espera}, Respuesta={proceso.tiempo_respuesta}")

    def _ejecutar_round_robin(self):
        """Round Robin con objetos Proceso"""
        quantum = 2
        procesos = list(self.cola_procesos)
        cola = deque(sorted(procesos, key=lambda x: x.instante_llegada))
        tiempo_actual = 0

        while cola and self.simulacion_activa:
            proceso = cola.popleft()
            
           
            if tiempo_actual < proceso.instante_llegada:
                tiempo_actual = proceso.instante_llegada

           
            if not proceso.ejecutado:
                proceso.tiempo_respuesta = tiempo_actual - proceso.instante_llegada
                proceso.ejecutado = True

            tiempo_ejecucion = min(quantum, proceso.tiempo_restante)
            self.mostrar(f"🔁 T{tiempo_actual}: {proceso.nombre} ejecuta {tiempo_ejecucion}u")

            for i in range(tiempo_ejecucion):
                if not self.simulacion_activa:
                    break
                tiempo_actual += 1
                proceso.tiempo_restante -= 1
                time.sleep(0.5 * self.velocidad)

                if proceso.tiempo_restante == 0:
                    proceso.tiempo_finalizacion = tiempo_actual
                    break

            if proceso.tiempo_restante > 0:
                cola.append(proceso)
                self.mostrar(f"   ↪️  {proceso.nombre} vuelve a cola ({proceso.tiempo_restante} restante)")
            else:
                tiempo_espera = proceso.tiempo_finalizacion - proceso.instante_llegada - proceso.tiempo_cpu
                proceso.tiempo_espera = max(0, tiempo_espera)
                self.mostrar(f"   ✅ {proceso.nombre} completado")

    def _mostrar_metricas_finales(self):
        """Muestra métricas finales de todos los procesos"""
        if not self.cola_procesos:
            return

        self.mostrar("\n📊 MÉTRICAS FINALES:")
        self.mostrar("─" * 40)
        
        for proceso in self.cola_procesos:
            if proceso.tiempo_finalizacion is not None:
                turnaround = proceso.tiempo_finalizacion - proceso.instante_llegada
                self.mostrar(f"PID {proceso.pid:3d} | {proceso.nombre:12s} | ")
                self.mostrar(f"Turnaround: {turnaround:3d} | Espera: {proceso.tiempo_espera:3d} | ")
                self.mostrar(f"Respuesta: {proceso.tiempo_respuesta or 'N/A':3}")

def ejecutar_simulacion(procesos, algoritmo, text_widget):
    """
    Función pública adaptada para usar con la clase Proceso
    """
    motor = MotorSimulacion(text_widget)

    
    for proceso in procesos:
        motor.agregar_proceso(proceso)

    thread = Thread(target=motor.iniciar, args=(algoritmo,))
    thread.daemon = True
    thread.start()

