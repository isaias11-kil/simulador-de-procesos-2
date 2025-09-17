import tkinter as tk
from tkinter import ttk, messagebox

class InterfazSimulador:
    def __init__(self, root, simulacion_callback):
        self.root = root
        self.root.title("Simulador de Planificación de Procesos")
        self.root.geometry("700x500")
        self.simulacion_callback = simulacion_callback

        # Lista local de procesos (se actualizará en la UI)
        self.procesos = []
        self.pid_counter = 1

        self.crear_widgets()

    def crear_widgets(self):
        # ---- Formulario de creación de procesos ----
        frame_form = ttk.LabelFrame(self.root, text="Crear Proceso")
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(frame_form)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Tiempo CPU:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_tiempo = ttk.Entry(frame_form)
        self.entry_tiempo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Instante de Llegada:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_llegada = ttk.Entry(frame_form)
        self.entry_llegada.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Quantum:").grid(row=1, column=2, padx=5, pady=5)
        self.entry_quantum = ttk.Entry(frame_form)
        self.entry_quantum.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(frame_form, text="Agregar Proceso", command=self.agregar_proceso).grid(row=2, column=0, columnspan=4, pady=10)

        # ---- Tabla de procesos ----
        frame_tabla = ttk.LabelFrame(self.root, text="Cola de Procesos")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)

        columnas = ("PID", "Nombre", "CPU", "Llegada", "Quantum")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor="center")

        self.tabla.pack(fill="both", expand=True)

        # ---- Selección de algoritmo ----
        frame_algo = ttk.LabelFrame(self.root, text="Algoritmo de Planificación")
        frame_algo.pack(fill="x", padx=10, pady=5)

        self.algoritmo = tk.StringVar(value="FCFS")
        opciones = ["FCFS", "SJF", "SRTF", "Round Robin"]
        self.combo_algoritmo = ttk.Combobox(frame_algo, textvariable=self.algoritmo, values=opciones, state="readonly")
        self.combo_algoritmo.pack(padx=5, pady=5)

        # ---- Botón de simulación ----
        ttk.Button(self.root, text="Iniciar Simulación", command=self.iniciar_simulacion).pack(pady=10)

    def agregar_proceso(self):
        try:
            nombre = self.entry_nombre.get()
            tiempo = int(self.entry_tiempo.get())
            llegada = int(self.entry_llegada.get())
            quantum = self.entry_quantum.get()
            quantum = int(quantum) if quantum else None

            proceso = {
                "PID": self.pid_counter,
                "Nombre": nombre,
                "CPU": tiempo,
                "Llegada": llegada,
                "Quantum": quantum
            }

            self.procesos.append(proceso)
            self.tabla.insert("", "end", values=(proceso["PID"], nombre, tiempo, llegada, quantum))
            self.pid_counter += 1

            # limpiar inputs
            self.entry_nombre.delete(0, tk.END)
            self.entry_tiempo.delete(0, tk.END)
            self.entry_llegada.delete(0, tk.END)
            self.entry_quantum.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")

    def iniciar_simulacion(self):
        if not self.procesos:
            messagebox.showwarning("Atención", "No hay procesos en la cola.")
            return

        algoritmo = self.algoritmo.get()
        # Aquí se llama al motor de simulación (Persona 3)
        self.simulacion_callback(self.procesos, algoritmo)


# ---- Para pruebas rápidas ----
if __name__ == "__main__":
    def simulacion_dummy(procesos, algoritmo):
        print("Iniciando simulación con algoritmo:", algoritmo)
        for p in procesos:
            print(p)

    root = tk.Tk()
    app = InterfazSimulador(root, simulacion_dummy)
    root.mainloop()