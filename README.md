# Simulador de Planificación de Procesos

Este proyecto es un simulador visual de algoritmos de planificación de procesos en sistemas operativos. Permite crear procesos, elegir el algoritmo de planificación, ejecutar la simulación y visualizar el historial y métricas de los procesos ejecutados.

---

## Tabla de Contenidos

- [Características](#características)
- [Instalación](#instalación)
- [Estructura de Archivos](#estructura-de-archivos)
- [Uso](#uso)
- [Algoritmos Soportados](#algoritmos-soportados)
- [Historial de Procesos](#historial-de-procesos)
- [Exportar Resultados](#exportar-resultados)
- [Créditos](#créditos)

---

## Características

- **Creación de procesos**: Agrega uno o varios procesos con nombre, tiempo de CPU, instante de llegada y quantum (si aplica).
- **Selección de algoritmo**: Elige entre FCFS, SJF, SRTF y Round Robin.
- **Simulación visual**: Muestra la cola de procesos y el avance de la simulación.
- **Historial en tiempo real**: Visualiza el historial de procesos ejecutados conforme avanzan.
- **Exportación**: Exporta historial y resultados a archivos de texto.
- **Métricas**: Calcula y muestra métricas como turnaround, espera y respuesta.

---

## Instalación

1. Clona el repositorio o descarga los archivos.
2. Asegúrate de tener Python 3 instalado.
3. Instala dependencias si es necesario (Tkinter viene por defecto en la mayoría de instalaciones de Python).

```sh
git clone <URL_DEL_REPOSITORIO>
cd simulador-de-procesos-2-main
python main.py
```

---

## Estructura de Archivos

- **main.py**  
  Punto de entrada principal. Integra la interfaz, historial y lógica de simulación.

- **interfaz.py**  
  Interfaz gráfica para crear procesos, configurar simulación y mostrar resultados.

- **procesos.py**  
  Clase `Proceso` y función para crear procesos con atributos relevantes.

- **algoritmos.py**  
  Implementación de algoritmos de planificación (FCFS, SJF, SRTF, Round Robin) y cálculo de métricas.

- **historial.py**  
  Módulo para mostrar y exportar el historial de procesos ejecutados.

- **simulacion.py**  
  Motor de simulación alternativo para ejecución paso a paso y visualización detallada.

---

## Uso

1. **Ejecuta `main.py`**  
   Se abrirá la ventana principal del simulador.

   <img width="1751" height="985" alt="simulador" src="https://github.com/user-attachments/assets/f05e447e-d1cd-4855-b892-7dc0b54c1f18" />


3. **Agrega procesos**  
   Completa los campos y presiona "Agregar Proceso". Los procesos aparecerán en la tabla.
   
   <img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/f54bde7d-7ac8-4383-8710-7fbfef00d01b" />

   <img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/b832f66b-609f-4b9b-8ad2-3eb19752fe4a" />

   <img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/0820ed4c-e56d-44a3-aaf4-29315d99cb26" />




5. **Selecciona el algoritmo**  
   Elige el algoritmo de planificación en el menú desplegable.

   <img width="796" height="350" alt="image" src="https://github.com/user-attachments/assets/dd53f828-6a91-44b5-bcdb-e0db5e819c46" />


7. **Inicia la simulación**  
   Presiona "🎯 Iniciar Simulación". Observa la ejecución y el historial en tiempo real.

8. **Exporta resultados o historial**  
   Usa los botones correspondientes para guardar la información en archivos de texto.

---

## Algoritmos Soportados

- **FCFS** (First Come First Served)
- **SJF** (Shortest Job First)
- **SRTF** (Shortest Remaining Time First)
- **Round Robin** (con quantum configurable)

---

## Historial de Procesos

El historial muestra cada proceso ejecutado, con detalles como PID, nombre, algoritmo, tiempos y estado. Se actualiza automáticamente conforme los procesos finalizan.

<img width="350" height="450" alt="image" src="https://github.com/user-attachments/assets/b9e9f595-1090-47d7-b4d2-2e8a772cb2eb" />



---

## Exportar Resultados

Puedes exportar tanto el historial como los resultados de la simulación a archivos `.txt` para su análisis o respaldo, unicamente debes presionar el boton Exportar Resultado o Exportar Historial y lueog deberas guardar el archivo en la ruta que deseas.

<img width="600" height="146" alt="image" src="https://github.com/user-attachments/assets/75a488c3-4c97-4722-907a-ea6b6585b756" />


---

## Créditos

Desarrollado por Grupo #7 |Sistemas Operativos|  


---
