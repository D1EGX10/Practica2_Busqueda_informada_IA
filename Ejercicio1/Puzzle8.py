#Empezamos
import heapq
import time
import psutil
import os
from collections import deque

class Nodo:
    def __init__(self, estado, padre, movimiento, profundidad, costo):
        self.estado = estado  
        self.padre = padre
        self.movimiento = movimiento
        self.profundidad = profundidad
        self.costo = costo 
    
    def __lt__(self, otro):
        return self.costo < otro.costo

class Puzzle8:
    def __init__(self, estado_inicial, estado_objetivo=(1,2,3,4,5,6,7,8,0)):
        self.inicial = estado_inicial
        self.objetivo = estado_objetivo
        self.metas_pos = {v: i for i, v in enumerate(estado_objetivo)}
        self.tamano = 3
        self.vecinos = [(-1,0), (1,0), (0,-1), (0,1)] 
    
    def obtener_vacio(self, estado):
        return estado.index(0)
    
    def mover(self, estado, vacio, direccion):
        """Genera nuevo estado moviendo el espacio vacío"""
        fila, col = divmod(vacio, self.tamano)
        df, dc = direccion
        nueva_f, nueva_c = fila + df, col + dc
        
        if 0 <= nueva_f < self.tamano and 0 <= nueva_c < self.tamano:
            nueva_pos = nueva_f * self.tamano + nueva_c
            nuevo_estado = list(estado)
            nuevo_estado[vacio], nuevo_estado[nueva_pos] = nuevo_estado[nueva_pos], nuevo_estado[vacio]
            return tuple(nuevo_estado)
        return None
    
    def generar_sucesores(self, nodo):
        """Genera todos los estados sucesores"""
        sucesores = []
        vacio = self.obtener_vacio(nodo.estado)
        
        for direccion in self.vecinos:
            nuevo_estado = self.mover(nodo.estado, vacio, direccion)
            if nuevo_estado:
                sucesores.append(Nodo(
                    nuevo_estado, 
                    nodo, 
                    direccion, 
                    nodo.profundidad + 1,
                    nodo.profundidad + 1 
                ))
        return sucesores
    
    # Heurística 1: Fichas fuera de lugar
    def heuristica_ffl(self, estado):
        """Cuenta cuántas fichas están en posición incorrecta (sin contar el 0)"""
        contador = 0
        for i in range(1, 9):  # del 1 al 8
            if estado[i] != self.objetivo[i]:
                contador += 1
        return contador
    
    # Heurística 2: Distancia Manhattan
    def heuristica_manhattan(self, estado):
        """Suma de distancias Manhattan de cada ficha a su posición objetivo"""
        distancia = 0
        for i, valor in enumerate(estado):
            if valor != 0:
                fila_actual, col_actual = divmod(i, self.tamano)
                pos_objetivo = self.metas_pos[valor]
                fila_objetivo, col_objetivo = divmod(pos_objetivo, self.tamano)
                distancia += abs(fila_actual - fila_objetivo) + abs(col_actual - col_objetivo)
        return distancia
    
    # Heurística 3: Heurística personalizada (Manhattan + Conflicto lineal)
    def heuristica_personalizada(self, estado):
        """
        Manhattan + Conflicto lineal
        El conflicto lineal cuenta cuando dos fichas están en la misma fila/columna
        pero en orden inverso, sumando 2 por cada par en conflicto
        """
        # Base Manhattan
        h = self.heuristica_manhattan(estado)
        
        # Conflicto lineal en filas
        for fila in range(self.tamano):
            fila_estado = []
            for col in range(self.tamano):
                idx = fila * self.tamano + col
                valor = estado[idx]
                if valor != 0:
                    pos_meta = self.metas_pos[valor]
                    fila_meta = pos_meta // self.tamano
                    if fila_meta == fila:  # Ficha pertenece a esta fila
                        fila_estado.append((valor, col))
            
            # Verificar pares en conflicto
            for i in range(len(fila_estado)):
                for j in range(i + 1, len(fila_estado)):
                    if fila_estado[i][1] > fila_estado[j][1]:
                        h += 2
        
        # Conflicto lineal en columnas
        for col in range(self.tamano):
            col_estado = []
            for fila in range(self.tamano):
                idx = fila * self.tamano + col
                valor = estado[idx]
                if valor != 0:
                    pos_meta = self.metas_pos[valor]
                    col_meta = pos_meta % self.tamano
                    if col_meta == col:  # Ficha pertenece a esta columna
                        col_estado.append((valor, fila))
            
            for i in range(len(col_estado)):
                for j in range(i + 1, len(col_estado)):
                    if col_estado[i][1] > col_estado[j][1]:
                        h += 2
        
        return h
    
    def a_estrella(self, heuristica_nombre):
        """Algoritmo A* con la heurística seleccionada"""
        # Seleccionar heurística
        if heuristica_nombre == "ffl":
            heuristica = self.heuristica_ffl
        elif heuristica_nombre == "manhattan":
            heuristica = self.heuristica_manhattan
        elif heuristica_nombre == "personalizada":
            heuristica = self.heuristica_personalizada
        else:
            raise ValueError("Heurística no válida")
        
        # Inicio de medición
        inicio_tiempo = time.time()
        proceso = psutil.Process(os.getpid())
        memoria_inicio = proceso.memory_info().rss / 1024  # KB
        
        # Nodo inicial
        nodo_inicial = Nodo(self.inicial, None, None, 0, heuristica(self.inicial))
        
        # Cola de prioridad (f(n) = g(n) + h(n))
        open_set = [(nodo_inicial.costo, nodo_inicial)]
        heapq.heapify(open_set)
        
        # Conjunto de estados visitados
        cerrado = set()
        
        # Diccionario para tracking
        nodos_generados = 0
        nodos_expandidos = 0
        
        while open_set:
            _, nodo_actual = heapq.heappop(open_set)
            nodos_expandidos += 1
            
            # Verificar si es objetivo
            if nodo_actual.estado == self.objetivo:
                # Reconstruir camino
                camino = []
                nodo = nodo_actual
                while nodo:
                    camino.append(nodo.movimiento)
                    nodo = nodo.padre
                camino.reverse()
                
                # Fin de medición
                memoria_fin = proceso.memory_info().rss / 1024
                tiempo_total = time.time() - inicio_tiempo
                memoria_usada = memoria_fin - memoria_inicio
                
                return {
                    'exito': True,
                    'camino': camino[1:],  # excluir None
                    'profundidad': nodo_actual.profundidad,
                    'nodos_generados': nodos_generados,
                    'nodos_expandidos': nodos_expandidos,
                    'tiempo': tiempo_total,
                    'memoria': memoria_usada,
                    'heuristica': heuristica_nombre
                }
            
            if nodo_actual.estado in cerrado:
                continue
            
            cerrado.add(nodo_actual.estado)
            
            # Generar sucesores
            for sucesor in self.generar_sucesores(nodo_actual):
                if sucesor.estado in cerrado:
                    continue
                g = sucesor.profundidad
                h_val = heuristica(sucesor.estado)
                f = g + h_val
                sucesor.costo = f
                
                heapq.heappush(open_set, (f, sucesor))
                nodos_generados += 1
        return {
            'exito': False,
            'nodos_generados': nodos_generados,
            'nodos_expandidos': nodos_expandidos,
            'tiempo': time.time() - inicio_tiempo,
            'memoria': 0,
            'heuristica': heuristica_nombre
        }

# Prueba
if __name__ == "__main__":
    # Estado inicial (fácil)
    inicial_facil = (1, 2, 3, 4, 0, 5, 7, 8, 6)
    
    # Estado inicial (más complejo)
    inicial_complejo = (2, 8, 3, 1, 6, 4, 7, 0, 5)
    
    print("=== PRUEBA 8-PUZZLE ===")
    puzzle = Puzzle8(inicial_complejo)
    
    for heur in ["ffl", "manhattan", "personalizada"]:
        print(f"\n--- Heurística: {heur} ---")
        resultado = puzzle.a_estrella(heur)
        
        if resultado['exito']:
            print(f"Solución encontrada")
            print(f"Profundidad: {resultado['profundidad']}")
            print(f"Nodos generados: {resultado['nodos_generados']}")
            print(f"Nodos expandidos: {resultado['nodos_expandidos']}")
            print(f"Tiempo: {resultado['tiempo']:.4f} segundos")
            print(f"Memoria: {resultado['memoria']:.2f} KB")
        else:
            print(f"No se encontró solución")