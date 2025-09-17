import tkinter as tk
from interfaz import InterfazSimulador
# Cuando Persona 3 haga el motor, se importa aquí:
# from simulacion import ejecutar_simulacion

def simulacion_callback(procesos, algoritmo):
    """
    Callback que recibe los procesos y el algoritmo seleccionado desde la interfaz.
    Aquí se conecta con el motor de simulación (Persona 3).
    """
    print(">>> Simulación iniciada <<<")
    print("Algoritmo seleccionado:", algoritmo)
    print("Procesos recibidos:")

    for p in procesos:
        print(p)

    # Aquí se llamará al motor de simulación real
    # resultado = ejecutar_simulacion(procesos, algoritmo)
    # print("Resultado de la simulación:", resultado)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazSimulador(root, simulacion_callback)
    root.mainloop()