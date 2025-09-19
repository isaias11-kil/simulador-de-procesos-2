import time
import tkinter as tk
from collections import deque
from threading import Thread

# Clase que representa un proceso
class Proceso:
    def __init__(self, nombre, tiempo_ejecucion):
        self.nombre = nombre
        self.tiempo_total = tiempo_ejecucion   # Duración total del proceso
        self.tiempo_restante = tiempo_ejecucion # Tiempo restante

    # Ejecutar un paso del proceso
    def ejecutar_un_paso(self):
        if self.tiempo_restante > 0:
            self.tiempo_restante -= 1
            return True  # Aún no ha terminado
        return False     # Proceso terminado

    def __str__(self):
        return f"{self.nombre} (Restante: {self.tiempo_restante})"


# Motor de simulación
class MotorSimulacion:
    def __init__(self, text_widget):
        self.cola_procesos = deque()  # Cola de procesos
        self.tiempo = 0               # Tiempo transcurrido
        self.text_widget = text_widget # Widget de tkinter donde mostrar la simulación
        self.simulacion_activa = False

    # Agregar proceso a la cola
    def agregar_proceso(self, proceso):
        self.cola_procesos.append(proceso)

    # Método para imprimir en el widget de tkinter
    def mostrar(self, texto):
        self.text_widget.insert(tk.END, texto + "\n")
        self.text_widget.see(tk.END)  # Desplazar automáticamente

    # Función que realiza la simulación paso a paso
    def iniciar(self):
        self.simulacion_activa = True
        self.mostrar("=== Iniciando Simulación ===")

        # Mientras haya procesos en la cola
        while self.cola_procesos and self.simulacion_activa:
            self.tiempo += 1

            # Ejecutar procesos siguiendo el algoritmo FIFO
            proceso_actual = self.cola_procesos[0]

            # Mostrar información del paso de tiempo
            self.mostrar(f"\nUnidad de tiempo {self.tiempo} → {self.tiempo*5} segundos")
            self.mostrar(f"Ejecutando: {proceso_actual}")

            # Ejecutar 1 paso del proceso
            if proceso_actual.ejecutar_un_paso():
                self.mostrar(f"Proceso {proceso_actual.nombre} aún no ha terminado.")
            else:
                self.mostrar(f"✅ Proceso {proceso_actual.nombre} ha finalizado.")
                self.cola_procesos.popleft()  # Quitar proceso terminado

            # Actualizar estado de la cola
            self.mostrar("Cola actual: " + ", ".join(str(p) for p in self.cola_procesos))

            # Simular paso de tiempo real
            time.sleep(1)

        self.mostrar("\n=== Simulación Terminada ===")
        self.simulacion_activa = False


# Función que se ejecuta al presionar el botón
def ejecutar_simulacion():
    # Crear motor con el widget de texto
    motor = MotorSimulacion(texto_simulacion)

    # Agregar procesos (nombre, duración)
    motor.agregar_proceso(Proceso("P1", 3))
    motor.agregar_proceso(Proceso("P2", 4))
    motor.agregar_proceso(Proceso("P3", 2))

    # Ejecutar simulación en un hilo para no bloquear la ventana
    thread = Thread(target=motor.iniciar)
    thread.start()


# =====================
# Interfaz gráfica con Tkinter
# =====================
ventana = tk.Tk()
ventana.title("Simulación de Procesos")

# Botón para iniciar la simulación
boton_iniciar = tk.Button(ventana, text="Iniciar Simulación", command=ejecutar_simulacion)
boton_iniciar.pack(pady=10)

# Widget de texto para mostrar la simulación
texto_simulacion = tk.Text(ventana, height=20, width=60)
texto_simulacion.pack(padx=10, pady=10)

# Ejecutar la ventana
ventana.mainloop()

