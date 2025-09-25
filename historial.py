# historial.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class HistorialUI(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.contador_simulaciones = 0
        self.crear_widgets()
    
    def crear_widgets(self):
        
        self.frame = ttk.LabelFrame(self, text="📊 Historial de Simulaciones")
        self.frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        
        self.label_contador = ttk.Label(self.frame, text="Simulaciones realizadas: 0")
        self.label_contador.pack(padx=5, pady=5, anchor="w")
        
        
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        

        self.lista_historial = tk.Listbox(list_frame, height=15, font=("Arial", 10))
        self.lista_historial.pack(side="left", fill="both", expand=True)
        
     
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.lista_historial.yview)
        scrollbar.pack(side="right", fill="y")
        self.lista_historial.config(yscrollcommand=scrollbar.set)
        
 
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(button_frame, text="Limpiar Historial", 
                  command=self.limpiar_historial).pack(side="left", padx=2)
        ttk.Button(button_frame, text="Exportar Historial", 
                  command=self.exportar_historial).pack(side="left", padx=2)
    
    def agregar_entrada(self, descripcion):
        """Agrega una nueva entrada al historial"""
        self.contador_simulaciones += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        entrada = f"{self.contador_simulaciones:02d}. [{timestamp}] {descripcion}"
        
        self.lista_historial.insert(tk.END, entrada)
        self.lista_historial.see(tk.END)  
        self.actualizar_contador()
    
    def limpiar_historial(self):
        """Limpia todo el historial"""
        if self.lista_historial.size() > 0:
            if messagebox.askyesno("Confirmar", "¿Está seguro de limpiar el historial?"):
                self.lista_historial.delete(0, tk.END)
                self.contador_simulaciones = 0
                self.actualizar_contador()
    
    def exportar_historial(self):
        """Exporta el historial a un archivo de texto"""
        if self.lista_historial.size() == 0:
            messagebox.showwarning("Advertencia", "El historial está vacío.")
            return
        
        try:
            from tkinter import filedialog
            archivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                title="Exportar historial"
            )
            
            if archivo:
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write("HISTORIAL DE SIMULACIONES\n")
                    f.write("=" * 50 + "\n")
                    for i in range(self.lista_historial.size()):
                        f.write(self.lista_historial.get(i) + "\n")
                
                messagebox.showinfo("Éxito", f"Historial exportado a:\n{archivo}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el historial:\n{str(e)}")
    
    def actualizar_contador(self):
        """Actualiza el contador de simulaciones"""
        self.label_contador.config(text=f"Simulaciones realizadas: {self.contador_simulaciones}")

