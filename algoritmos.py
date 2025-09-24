from collections import deque
import copy

def FCFS(procesos):
    """
    First Come First Served (FCFS)
    No expropiativo
    """
    # Ordenar procesos por tiempo de llegada
    procesos_ordenados = sorted(procesos, key=lambda x: x.tiempo_llegada)
    tiempo_actual = 0
    resultado = []
    
    for proceso in procesos_ordenados:
        # Esperar si el proceso aún no ha llegado
        if tiempo_actual < proceso.tiempo_llegada:
            tiempo_actual = proceso.tiempo_llegada
        
        # Ejecutar el proceso
        inicio = tiempo_actual
        fin = tiempo_actual + proceso.tiempo_rafaga
        resultado.append({
            'proceso': proceso.id,
            'inicio': inicio,
            'fin': fin,
            'duracion': proceso.tiempo_rafaga
        })
        
        tiempo_actual = fin
        proceso.tiempo_finalizacion = fin
        proceso.tiempo_espera = inicio - proceso.tiempo_llegada
    
    return resultado

def SJF(procesos):
    """
    Shortest Job First (SJF) - No expropiativo
    """
    procesos = copy.deepcopy(procesos)
    procesos_restantes = sorted(procesos, key=lambda x: x.tiempo_llegada)
    tiempo_actual = 0
    resultado = []
    cola_listos = []
    
    while procesos_restantes or cola_listos:
        # Agregar procesos que han llegado a la cola de listos
        while procesos_restantes and procesos_restantes[0].tiempo_llegada <= tiempo_actual:
            cola_listos.append(procesos_restantes.pop(0))
        
        if cola_listos:
            # Ordenar por tiempo de ráfaga (más corto primero)
            cola_listos.sort(key=lambda x: x.tiempo_rafaga)
            proceso = cola_listos.pop(0)
            
            inicio = tiempo_actual
            fin = tiempo_actual + proceso.tiempo_rafaga
            resultado.append({
                'proceso': proceso.id,
                'inicio': inicio,
                'fin': fin,
                'duracion': proceso.tiempo_rafaga
            })
            
            tiempo_actual = fin
            proceso.tiempo_finalizacion = fin
            proceso.tiempo_espera = inicio - proceso.tiempo_llegada
        else:
            # Si no hay procesos listos, avanzar al siguiente tiempo de llegada
            if procesos_restantes:
                tiempo_actual = procesos_restantes[0].tiempo_llegada
    
    return resultado

def SRTF(procesos):
    """
    Shortest Remaining Time First (SRTF) - Expropriativo
    """
    procesos = copy.deepcopy(procesos)
    procesos_restantes = sorted(procesos, key=lambda x: x.tiempo_llegada)
    tiempo_actual = 0
    resultado = []
    proceso_actual = None
    tiempo_inicio = None
    
    while procesos_restantes or proceso_actual:
        # Agregar procesos que han llegado
        procesos_llegados = [p for p in procesos_restantes if p.tiempo_llegada <= tiempo_actual]
        for p in procesos_llegados:
            procesos_restantes.remove(p)
        
        # Buscar el proceso con menor tiempo restante
        candidatos = procesos_llegados.copy()
        if proceso_actual:
            candidatos.append(proceso_actual)
        
        if candidatos:
            candidatos.sort(key=lambda x: x.tiempo_restante)
            nuevo_proceso = candidatos[0]
            
            # Si hay cambio de proceso
            if nuevo_proceso != proceso_actual:
                if proceso_actual and proceso_actual.tiempo_restante > 0:
                    # Guardar el segmento del proceso anterior
                    resultado.append({
                        'proceso': proceso_actual.id,
                        'inicio': tiempo_inicio,
                        'fin': tiempo_actual,
                        'duracion': tiempo_actual - tiempo_inicio
                    })
                
                proceso_actual = nuevo_proceso
                tiempo_inicio = tiempo_actual
            
            # Ejecutar 1 unidad de tiempo
            proceso_actual.tiempo_restante -= 1
            tiempo_actual += 1
            
            # Si el proceso termina
            if proceso_actual.tiempo_restante == 0:
                resultado.append({
                    'proceso': proceso_actual.id,
                    'inicio': tiempo_inicio,
                    'fin': tiempo_actual,
                    'duracion': tiempo_actual - tiempo_inicio
                })
                proceso_actual.tiempo_finalizacion = tiempo_actual
                proceso_actual.tiempo_espera = proceso_actual.tiempo_finalizacion - proceso_actual.tiempo_llegada - proceso_actual.tiempo_rafaga
                proceso_actual = None
        else:
            tiempo_actual += 1
    
    return resultado

def RoundRobin(procesos, quantum=2):
    """
    Round Robin con quantum
    """
    procesos = copy.deepcopy(procesos)
    procesos_restantes = sorted(procesos, key=lambda x: x.tiempo_llegada)
    tiempo_actual = 0
    resultado = []
    cola = deque()
    
    while procesos_restantes or cola:
        # Agregar procesos que han llegado
        while procesos_restantes and procesos_restantes[0].tiempo_llegada <= tiempo_actual:
            cola.append(procesos_restantes.pop(0))
        
        if cola:
            proceso = cola.popleft()
            inicio = tiempo_actual
            
            # Ejecutar por quantum o hasta que termine
            tiempo_ejecucion = min(quantum, proceso.tiempo_restante)
            fin = tiempo_actual + tiempo_ejecucion
            proceso.tiempo_restante -= tiempo_ejecucion
            
            resultado.append({
                'proceso': proceso.id,
                'inicio': inicio,
                'fin': fin,
                'duracion': tiempo_ejecucion
            })
            
            tiempo_actual = fin
            
            # Agregar procesos que llegaron durante la ejecución
            while procesos_restantes and procesos_restantes[0].tiempo_llegada <= tiempo_actual:
                cola.append(procesos_restantes.pop(0))
            
            # Si el proceso no ha terminado, volver a la cola
            if proceso.tiempo_restante > 0:
                cola.append(proceso)
            else:
                proceso.tiempo_finalizacion = tiempo_actual
                proceso.tiempo_espera = proceso.tiempo_finalizacion - proceso.tiempo_llegada - proceso.tiempo_rafaga
        else:
            tiempo_actual += 1
    
    return resultado
