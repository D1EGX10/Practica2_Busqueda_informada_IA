#Empezamos
import heapq
import time
import psutil
import os

class Nodo15:
    def __init__(self, estado, padre, movimiento, profundidad, costo):
        self.estado = estado
        self.padre = padre
        self.movimiento = movimiento
        self.profundidad = profundidad
        self.costo = costo
    
    def __lt__(self, otro):
        return self.costo < otro.costo

class Puzzle15:
    def __init__(self, estado_inicial, estado_objetivo=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)):
        self.inicial = estado_inicial
        self.objetivo = estado_objetivo
        self.metas_pos = {v: i for i, v in enumerate(estado_objetivo)}
        self.tamano = 4
        self.vecinos = [(-1,0), (1,0), (0,-1), (0,1)]
    
    def obtener_vacio(self, estado):
        return estado.index(0)
    
    def mover(self, estado, vacio, direccion):
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
        sucesores = []
        vacio = self.obtener_vacio(nodo.estado)
        
        for direccion in self.vecinos:
            nuevo_estado = self.mover(nodo.estado, vacio, direccion)
            if nuevo_estado:
                sucesores.append(Nodo15(
                    nuevo_estado, nodo, direccion, 
                    nodo.profundidad + 1, nodo.profundidad + 1
                ))
        return sucesores
    
    def heuristica_ffl(self, estado):
        """Fichas fuera de lugar (sin contar el 0)"""
        contador = 0
        for i in range(1, 16):  # del 1 al 15
            if estado[i] != self.objetivo[i]:
                contador += 1
        return contador
    
    def heuristica_manhattan(self, estado):
        """Distancia Manhattan"""
        distancia = 0
        for i, valor in enumerate(estado):
            if valor != 0:
                fila_actual, col_actual = divmod(i, self.tamano)
                pos_objetivo = self.metas_pos[valor]
                fila_objetivo, col_objetivo = divmod(pos_objetivo, self.tamano)
                distancia += abs(fila_actual - fila_objetivo) + abs(col_actual - col_objetivo)
        return distancia
    
    def heuristica_personalizada(self, estado):
        """
        Manhattan + Conflicto lineal optimizado para 15-puzzle
        """
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
                    if fila_meta == fila:
                        fila_estado.append((valor, col))
            
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
                    if col_meta == col:
                        col_estado.append((valor, fila))
            
            for i in range(len(col_estado)):
                for j in range(i + 1, len(col_estado)):
                    if col_estado[i][1] > col_estado[j][1]:
                        h += 2
        
        return h
    
    def a_estrella(self, heuristica_nombre, max_nodos=500000):
        """A* con límite de nodos para 15-puzzle"""
        if heuristica_nombre == "ffl":
            heuristica = self.heuristica_ffl
        elif heuristica_nombre == "manhattan":
            heuristica = self.heuristica_manhattan
        elif heuristica_nombre == "personalizada":
            heuristica = self.heuristica_personalizada
        else:
            raise ValueError("Heurística no válida")
        
        inicio_tiempo = time.time()
        proceso = psutil.Process(os.getpid())
        memoria_inicio = proceso.memory_info().rss / 1024
        
        nodo_inicial = Nodo15(self.inicial, None, None, 0, heuristica(self.inicial))
        open_set = [(nodo_inicial.costo, nodo_inicial)]
        heapq.heapify(open_set)
        
        cerrado = set()
        padres = {}
        
        nodos_generados = 1
        nodos_expandidos = 0
        
        while open_set and nodos_generados < max_nodos:
            _, nodo_actual = heapq.heappop(open_set)
            nodos_expandidos += 1
            
            if nodo_actual.estado == self.objetivo:
                camino = []
                nodo = nodo_actual
                while nodo:
                    camino.append(nodo.movimiento)
                    nodo = nodo.padre
                camino.reverse()
                
                memoria_fin = proceso.memory_info().rss / 1024
                tiempo_total = time.time() - inicio_tiempo
                
                return {
                    'exito': True,
                    'camino': camino[1:],
                    'profundidad': nodo_actual.profundidad,
                    'nodos_generados': nodos_generados,
                    'nodos_expandidos': nodos_expandidos,
                    'tiempo': tiempo_total,
                    'memoria': memoria_fin - memoria_inicio,
                    'heuristica': heuristica_nombre
                }
            
            if nodo_actual.estado in cerrado:
                continue
            
            cerrado.add(nodo_actual.estado)
            padres[nodo_actual.estado] = nodo_actual.padre
            
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


if __name__ == "__main__":
    # Estado inicial para 15-puzzle (fácil)
    inicial_facil = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15)
    
    # Estado inicial más complejo
    inicial_complejo = (5, 1, 2, 3, 9, 6, 7, 4, 13, 10, 11, 8, 0, 14, 15, 12)
    
    print("=== PRUEBA 15-PUZZLE ===")
    print("NOTA: El 15-puzzle puede tomar más tiempo, especialmente con FFL")
    
    puzzle = Puzzle15(inicial_complejo)
    
    for heur in ["manhattan", "personalizada"]:
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
            print(f"No se encontró solución (límite de nodos alcanzado)")