import time
import psutil
import os
import sys
from puzzle8 import Puzzle8
from puzzle15 import Puzzle15

def medir_memoria(func, *args, **kwargs):
    """Mide memoria antes y después de ejecutar la función"""
    proceso = psutil.Process(os.getpid())
    memoria_antes = proceso.memory_info().rss / 1024  # KB
    
    inicio = time.time()
    resultado = func(*args, **kwargs)
    tiempo = time.time() - inicio
    
    memoria_despues = proceso.memory_info().rss / 1024
    memoria_usada = memoria_despues - memoria_antes
    
    return resultado, tiempo, memoria_usada

def tabla_comparativa_8puzzle():
    """Genera tabla comparativa para 8-puzzle"""
    print("\n" + "="*80)
    print("COMPARATIVA 8-PUZZLE".center(80))
    print("="*80)
    
    # Estados de prueba
    estados = {
        "Fácil": (1, 2, 3, 4, 0, 5, 7, 8, 6),
        "Medio": (2, 8, 3, 1, 6, 4, 7, 0, 5),
        "Difícil": (2, 8, 1, 0, 4, 3, 7, 6, 5)
    }
    
    heuristicas = ["ffl", "manhattan", "personalizada"]
    
    # Encabezado
    print(f"\n{'Estado':<10} {'Heurística':<15} {'Éxito':<6} {'Profundidad':<12} {'Nodos Gen':<12} {'Nodos Exp':<12} {'Tiempo (s)':<12} {'Memoria (KB)':<12}")
    print("-"*95)
    
    for nombre_estado, estado_inicial in estados.items():
        for heur in heuristicas:
            puzzle = Puzzle8(estado_inicial)
            
            try:
                resultado, tiempo, memoria = medir_memoria(puzzle.a_estrella, heur)
                
                exito = "SI JALO" if resultado['exito'] else "NO JALO"
                profundidad = resultado.get('profundidad', '-')
                nodos_gen = resultado.get('nodos_generados', '-')
                nodos_exp = resultado.get('nodos_expandidos', '-')
                
                print(f"{nombre_estado:<10} {heur:<15} {exito:<6} {profundidad:<12} {nodos_gen:<12} {nodos_exp:<12} {tiempo:<12.4f} {memoria:<12.2f}")
                
            except Exception as e:
                print(f"{nombre_estado:<10} {heur:<15} {'NEL':<6} {'Error':<12} {'-':<12} {'-':<12} {'-':<12} {'-':<12}")
                print(f"  Error: {e}")

def tabla_comparativa_15puzzle():
    """Genera tabla comparativa para 15-puzzle"""
    print("\n" + "="*80)
    print("COMPARATIVA 15-PUZZLE".center(80))
    print("="*80)
    
    estados = {
        "Fácil": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15),
        "Medio": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 14, 15),
        "Difícil": (5, 1, 2, 3, 9, 6, 7, 4, 13, 10, 11, 8, 0, 14, 15, 12)
    }
    
    heuristicas = ["manhattan", "personalizada"]  # FFL es demasiado lento para 15-puzzle
    
    print(f"\n{'Estado':<10} {'Heurística':<15} {'Éxito':<6} {'Profundidad':<12} {'Nodos Gen':<12} {'Nodos Exp':<12} {'Tiempo (s)':<12} {'Memoria (KB)':<12}")
    print("-"*95)
    
    for nombre_estado, estado_inicial in estados.items():
        for heur in heuristicas:
            puzzle = Puzzle15(estado_inicial)
            
            try:
                resultado, tiempo, memoria = medir_memoria(puzzle.a_estrella, heur)
                
                exito = "SI JALO" if resultado['exito'] else "NO JALO"
                profundidad = resultado.get('profundidad', '-')
                nodos_gen = resultado.get('nodos_generados', '-')
                nodos_exp = resultado.get('nodos_expandidos', '-')
                
                print(f"{nombre_estado:<10} {heur:<15} {exito:<6} {profundidad:<12} {nodos_gen:<12} {nodos_exp:<12} {tiempo:<12.4f} {memoria:<12.2f}")
                
            except Exception as e:
                print(f"{nombre_estado:<10} {heur:<15} {'❌':<6} {'Error':<12} {'-':<12} {'-':<12} {'-':<12} {'-':<12}")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("PRÁCTICA 2 - EJERCICIO 1".center(80))
    print("Comparativa de heurísticas para 8-puzzle y 15-puzzle")
    print("="*80)
    
    tabla_comparativa_8puzzle()
    tabla_comparativa_15puzzle()