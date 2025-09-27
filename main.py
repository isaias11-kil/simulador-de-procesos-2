from interfaz import InterfazSimulador
from historial import HistorialUI
from procesos import Proceso
from algoritmos import FabricaAlgoritmos
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread

class SimuladorAvanzado:
    """Clase principal que integra todos los componentes"""
    
    def __init__(self, root):
        self.root = root
        self.historial_ui = None
        self.interfaz = None
        self.configurar_ventana()
        self.crear_componentes()
    
    def configurar_ventana(self):
        self.root.title("Simulador Avanzado de Planificación de Procesos")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
    
    def crear_componentes(self):
     
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        
        self.historial_ui = HistorialUI(main_frame)
        self.historial_ui.pack(side="right", fill="both", padx=(10, 0), pady=10)
        
    
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=10)
        
       
        callback = self.crear_callback_simulacion()
        self.interfaz = InterfazSimulador(left_frame, callback)
        self.interfaz.pack(fill="both", expand=True)
        
      
        self.crear_barra_estado()
    
    def crear_callback_simulacion(self):
        def callback(procesos, algoritmo, text_widget):
            self.ejecutar_simulacion_avanzada(procesos, algoritmo, text_widget)
        return callback
    
    def ejecutar_simulacion_avanzada(self, procesos, algoritmo, text_widget):
        """Ejecuta simulación usando el módulo de algoritmos"""
        def ejecutar():
            try:
                text_widget.delete(1.0, tk.END)
                
               
                text_widget.insert(tk.END, "═" * 60 + "\n")
                text_widget.insert(tk.END, f"           SIMULACIÓN CON ALGORITMO: {algoritmo}\n")
                text_widget.insert(tk.END, "═" * 60 + "\n")
                text_widget.insert(tk.END, f"Procesos a simular: {len(procesos)}\n")
                text_widget.insert(tk.END, "─" * 60 + "\n\n")
                
              
                procesos_objetos = []
                text_widget.insert(tk.END, "🔄 CREANDO PROCESOS...\n")
                
                for i, p_dict in enumerate(procesos, 1):
                    proceso = Proceso(
                        p_dict["Nombre"],
                        p_dict["CPU"],
                        p_dict["Llegada"],
                        p_dict["Quantum"]
                    )
                    procesos_objetos.append(proceso)
                    text_widget.insert(tk.END, f"   ✅ {proceso.nombre} (PID: {proceso.pid})\n")
                
               
                if self.historial_ui:
                    self.historial_ui.agregar_entrada(f"{algoritmo} - {len(procesos)} procesos")
                
               
                fabrica = FabricaAlgoritmos()
                algoritmo_obj = fabrica.crear_algoritmo(algoritmo)
                
                text_widget.insert(tk.END, f"\n🎯 INICIANDO {algoritmo}...\n")
                text_widget.insert(tk.END, "─" * 50 + "\n")
                
             
                eventos = algoritmo_obj.ejecutar(procesos_objetos)
                
            
                for evento in eventos:
                    text_widget.insert(tk.END, f"T{evento['tiempo']:3d}: {evento['evento']}\n")
                
          
                if self.historial_ui:
                    for proceso in procesos_objetos:
                        if proceso.tiempo_finalizacion is not None:
                            info = (f"{proceso.nombre} (PID: {proceso.pid}) | "
                                    f"Llegada: {proceso.instante_llegada} | "
                                    f"Finalización: {proceso.tiempo_finalizacion} | "
                                    f"Espera: {proceso.tiempo_espera} | "
                                    f"Retorno: {proceso.tiempo_finalizacion - proceso.instante_llegada}")
                            self.historial_ui.agregar_entrada(info)
                
                
                text_widget.insert(tk.END, "\n📊 MÉTRICAS FINALES:\n")
                text_widget.insert(tk.END, "─" * 40 + "\n")
                
                metricas = algoritmo_obj.metricas
                if metricas:
                    text_widget.insert(tk.END, f"• Throughput: {metricas.get('throughput', 0)} procesos\n")
                    text_widget.insert(tk.END, f"• Tiempo de retorno promedio: {metricas.get('tiempo_retorno_promedio', 0):.2f}u\n")
                    text_widget.insert(tk.END, f"• Tiempo de espera promedio: {metricas.get('tiempo_espera_promedio', 0):.2f}u\n")
                    text_widget.insert(tk.END, f"• Tiempo de respuesta promedio: {metricas.get('tiempo_respuesta_promedio', 0):.2f}u\n")
                    text_widget.insert(tk.END, f"• Uso de CPU: {metricas.get('uso_cpu', 0)*100:.1f}%\n")
                else:
                    text_widget.insert(tk.END, "No se pudieron calcular las métricas\n")
                
                text_widget.insert(tk.END, "\n" + "═" * 60 + "\n")
                text_widget.insert(tk.END, "           SIMULACIÓN COMPLETADA EXITOSAMENTE\n")
                text_widget.insert(tk.END, "═" * 60 + "\n")
                
            except Exception as e:
                error_msg = f"Error en simulación: {str(e)}"
                messagebox.showerror("Error", error_msg)
                text_widget.insert(tk.END, f"\n❌ {error_msg}\n")
        
   
        thread = Thread(target=ejecutar)
        thread.daemon = True
        thread.start()
    
    def crear_barra_estado(self):
        status_bar = ttk.Label(self.root, 
                              text="✅ Simulador avanzado listo - Módulo de algoritmos integrado", 
                              relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")


class SimuladorSimplificado:
   
    
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Planificación de Procesos")
        self.root.geometry("1200x700")
        

        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        from interfaz import InterfazSimulador
        self.interfaz = InterfazSimulador(main_frame, self.simulacion_callback)
        self.interfaz.pack(fill="both", expand=True)
    
    def simulacion_callback(self, procesos, algoritmo, text_widget):
        """Callback simple para simulación"""
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"Simulando {len(procesos)} procesos con {algoritmo}\n\n")
        
        for i, proceso in enumerate(procesos, 1):
            text_widget.insert(tk.END, f"{i}. {proceso['Nombre']} - CPU: {proceso['CPU']} - Llegada: {proceso['Llegada']}\n")
        
        text_widget.insert(tk.END, "\n✅ Simulación básica completada\n")

if __name__ == "__main__":
    root = tk.Tk()
    
    try:
     
        app = SimuladorAvanzado(root)
    except Exception as e:
        print(f"Error con SimuladorAvanzado: {e}")
        print("Usando versión simplificada...")
   
        app = SimuladorSimplificado(root)
    
    root.mainloop()
