import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


class InterfazSimulador(ttk.Frame):
    def __init__(self, parent, simulacion_callback):
        super().__init__(parent)
        self.simulacion_callback = simulacion_callback

  
        self.procesos = []
        self.pid_counter = 1

        self.crear_widgets()

    def crear_widgets(self):
      
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

      
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

  
        frame_form = ttk.LabelFrame(left_frame, text="Crear Proceso")
        frame_form.pack(fill="x", padx=5, pady=5)


        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = ttk.Entry(frame_form, width=15)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Tiempo CPU:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_tiempo = ttk.Entry(frame_form, width=10)
        self.entry_tiempo.grid(row=0, column=3, padx=5, pady=5)

     
        ttk.Label(frame_form, text="Instante de Llegada:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_llegada = ttk.Entry(frame_form, width=10)
        self.entry_llegada.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Quantum:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_quantum = ttk.Entry(frame_form, width=10)
        self.entry_quantum.grid(row=1, column=3, padx=5, pady=5)

      
        button_frame = ttk.Frame(frame_form)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Agregar Proceso", command=self.agregar_proceso).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Limpiar Campos", command=self.limpiar_campos).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Eliminar Seleccionado", command=self.eliminar_proceso).pack(side="left", padx=5)


        frame_tabla = ttk.LabelFrame(left_frame, text=f"Cola de Procesos (0 procesos)")
        frame_tabla.pack(fill="both", expand=True, padx=5, pady=5)

      
        table_container = ttk.Frame(frame_tabla)
        table_container.pack(fill="both", expand=True)

        columnas = ("PID", "Nombre", "CPU", "Llegada", "Quantum")
        self.tabla = ttk.Treeview(table_container, columns=columnas, show="headings", height=10)

        column_widths = {"PID": 60, "Nombre": 100, "CPU": 80, "Llegada": 100, "Quantum": 80}
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=column_widths[col], anchor="center")


        scrollbar_tabla = ttk.Scrollbar(table_container, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar_tabla.set)
        
        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar_tabla.pack(side="right", fill="y")


        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        frame_algo = ttk.LabelFrame(right_frame, text="Configuración de Simulación")
        frame_algo.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame_algo, text="Algoritmo de Planificación:").pack(anchor="w", padx=5, pady=2)
        self.algoritmo = tk.StringVar(value="FCFS")
        opciones = ["FCFS", "SJF", "SRTF", "Round Robin", "Prioridades"]
        self.combo_algoritmo = ttk.Combobox(frame_algo, textvariable=self.algoritmo, values=opciones, state="readonly")
        self.combo_algoritmo.pack(fill="x", padx=5, pady=5)

    
        stats_frame = ttk.Frame(frame_algo)
        stats_frame.pack(fill="x", padx=5, pady=5)
        
        self.label_stats = ttk.Label(stats_frame, text="Procesos: 0 | Tiempo total: 0")
        self.label_stats.pack(anchor="w")


        ttk.Button(frame_algo, text="🎯 Iniciar Simulación", command=self.iniciar_simulacion).pack(fill="x", padx=5, pady=10)

        # ---- Área de simulación mejorada ----
        frame_sim = ttk.LabelFrame(right_frame, text="Resultados de la Simulación")
        frame_sim.pack(fill="both", expand=True, padx=5, pady=5)

        self.texto_simulacion = scrolledtext.ScrolledText(frame_sim, height=20, wrap=tk.WORD, font=("Consolas", 10))
        self.texto_simulacion.pack(fill="both", expand=True, padx=5, pady=5)


        text_controls = ttk.Frame(frame_sim)
        text_controls.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(text_controls, text="Limpiar Resultados", command=self.limpiar_resultados).pack(side="left", padx=5)
        ttk.Button(text_controls, text="Exportar Resultados", command=self.exportar_resultados).pack(side="left", padx=5)

    def actualizar_estadisticas(self):
        """Actualiza las estadísticas de procesos"""
        total_procesos = len(self.procesos)
        tiempo_total = sum(p["CPU"] for p in self.procesos)
        self.label_stats.config(text=f"Procesos: {total_procesos} | Tiempo total: {tiempo_total}")
        
 
        for widget in self.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and "Cola de Procesos" in widget.cget("text"):
                widget.config(text=f"Cola de Procesos ({total_procesos} procesos)")

    def agregar_proceso(self):
        try:
            nombre = self.entry_nombre.get().strip()
            tiempo = int(self.entry_tiempo.get())
            llegada = int(self.entry_llegada.get())
            quantum = self.entry_quantum.get()
            quantum = int(quantum) if quantum else 0

            if tiempo <= 0:
                messagebox.showerror("Error", "El tiempo de CPU debe ser mayor a 0.")
                return

            if llegada < 0:
                messagebox.showerror("Error", "El instante de llegada no puede ser negativo.")
                return

            if not nombre:
                messagebox.showerror("Error", "El nombre del proceso no puede estar vacío.")
                return

            proceso = {
                "PID": self.pid_counter,
                "Nombre": nombre,
                "CPU": tiempo,
                "Llegada": llegada,
                "Quantum": quantum if quantum > 0 else None
            }

            self.procesos.append(proceso)
            self.tabla.insert("", "end", values=(
                proceso["PID"], 
                nombre, 
                tiempo, 
                llegada, 
                quantum if quantum > 0 else "N/A"
            ))
            self.pid_counter += 1

            self.limpiar_campos()
            self.actualizar_estadisticas()

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos (números enteros).")

    def eliminar_proceso(self):
        seleccionado = self.tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un proceso para eliminar.")
            return

        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar el proceso seleccionado?"):
            item = seleccionado[0]
            valores = self.tabla.item(item, "values")
            pid = int(valores[0])
            
       
            self.procesos = [p for p in self.procesos if p["PID"] != pid]
            
            self.tabla.delete(item)
            self.actualizar_estadisticas()

    def limpiar_campos(self):
        """Limpia los campos del formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_tiempo.delete(0, tk.END)
        self.entry_llegada.delete(0, tk.END)
        self.entry_quantum.delete(0, tk.END)
        self.entry_nombre.focus()

    def limpiar_resultados(self):
        """Limpia el área de resultados"""
        self.texto_simulacion.delete(1.0, tk.END)

    def exportar_resultados(self):
        """Exporta los resultados a un archivo de texto"""
        try:
            contenido = self.texto_simulacion.get(1.0, tk.END)
            if len(contenido.strip()) == 0:
                messagebox.showwarning("Advertencia", "No hay resultados para exportar.")
                return
            
            from tkinter import filedialog
            archivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if archivo:
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write(contenido)
                messagebox.showinfo("Éxito", f"Resultados exportados a: {archivo}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    def iniciar_simulacion(self):
        if not self.procesos:
            messagebox.showwarning("Atención", "No hay procesos en la cola.")
            return

        algoritmo = self.algoritmo.get()
        
   
        if algoritmo == "Round Robin":
            procesos_sin_quantum = [p for p in self.procesos if p["Quantum"] is None]
            if procesos_sin_quantum:
                messagebox.showwarning(
                    "Advertencia", 
                    "Algoritmo Round Robin requiere quantum definido para todos los procesos.\n"
                    "Los procesos sin quantum usarán valor por defecto."
                )

 
        self.limpiar_resultados()
        
     
        self.simulacion_callback(self.procesos, algoritmo, self.texto_simulacion)

    def set_callback(self, nuevo_callback):
        """Permite actualizar el callback de simulación"""
        self.simulacion_callback = nuevo_callback


if __name__ == "__main__":
    def simulacion_dummy(procesos, algoritmo, text_widget):
        text_widget.insert("end", f"=== SIMULACIÓN CON {algoritmo} ===\n")
        text_widget.insert("end", f"Procesos simulados: {len(procesos)}\n")
        text_widget.insert("end", "-" * 40 + "\n")
        for p in procesos:
            text_widget.insert("end", f"PID {p['PID']}: {p['Nombre']} (CPU: {p['CPU']}, Llegada: {p['Llegada']})\n")
        text_widget.insert("end", "Simulación completada.\n\n")

    root = tk.Tk()
    root.title("Simulador de Planificación de Procesos - Prueba")
    root.geometry("900x700")
    
    app = InterfazSimulador(root, simulacion_dummy)
    root.mainloop()
