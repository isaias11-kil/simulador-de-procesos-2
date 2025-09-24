def update_ui(self, current_time, executing, ready, completed):
        self.title(f"Tiempo: {current_time}")
        self.label_exec.config(text=f"{executing}" if executing else "Ninguno")

        # Actualizar lista de listos
        self.ready_list.delete(0, "end")
        for p in ready:
            self.ready_list.insert("end", str(p))

        # Actualizar historial
        self.hist_list.delete(0, "end")
        for p in completed:
            self.hist_list.insert("end", f"{p.name} (PID={p.pid}) terminado en t={p.finish_time}")
