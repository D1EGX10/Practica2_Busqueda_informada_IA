import time
from Puzzle8 import Puzzle8
from Puzzle15 import Puzzle15

def tabla_comparativa_8puzzle():
    print("\n" + "="*90)
    print("COMPARATIVA 8-PUZZLE".center(90))
    print("="*90)
    
    estados = {
        "Facil": (1, 2, 3, 4, 0, 5, 7, 8, 6),
        "Medio": (2, 8, 3, 1, 6, 4, 7, 0, 5),
        "Dificil": (2, 8, 1, 0, 4, 3, 7, 6, 5)
    }
    
    heuristicas = ["ffl", "manhattan", "personalizada"]
    
    print(f"\n{'Estado':<10} {'Heuristica':<15} {'Exito':<8} {'Profundidad':<12} {'Nodos Gen':<12} {'Nodos Exp':<12} {'Tiempo(s)':<12}")
    print("-"*85)
    
    for nombre_estado, estado_inicial in estados.items():
        for heur in heuristicas:
            puzzle = Puzzle8(estado_inicial)
            
            resultado = puzzle.a_estrella(heur)
            
            if resultado.get('exito', False):
                exito = "SI"
                profundidad = resultado['profundidad']
                nodos_gen = resultado['nodos_generados']
                nodos_exp = resultado['nodos_expandidos']
                tiempo = f"{resultado['tiempo']:.4f}"
            elif 'error' in resultado:
                exito = "NO"
                profundidad = "ERROR"
                nodos_gen = "-"
                nodos_exp = "-"
                tiempo = "-"
            else:
                exito = "NO"
                profundidad = "-"
                nodos_gen = resultado.get('nodos_generados', '-')
                nodos_exp = resultado.get('nodos_expandidos', '-')
                tiempo = f"{resultado.get('tiempo', 0):.4f}" if isinstance(resultado.get('tiempo', 0), (int, float)) else "-"
            
            print(f"{nombre_estado:<10} {heur:<15} {exito:<8} {str(profundidad):<12} {str(nodos_gen):<12} {str(nodos_exp):<12} {tiempo:<12}")

def tabla_comparativa_15puzzle():
    print("\n" + "="*90)
    print("COMPARATIVA 15-PUZZLE".center(90))
    print("="*90)
    
    estados = {
        "Facil": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 0, 15),
        "Medio": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0, 14, 15),
        "Dificil": (5, 1, 2, 3, 9, 6, 7, 4, 13, 10, 11, 8, 0, 14, 15, 12)
    }
    
    heuristicas = ["ffl", "manhattan", "personalizada"]
    
    print(f"\n{'Estado':<10} {'Heuristica':<15} {'Exito':<8} {'Profundidad':<12} {'Nodos Gen':<12} {'Nodos Exp':<12} {'Tiempo(s)':<12}")
    print("-"*85)
    
    for nombre_estado, estado_inicial in estados.items():
        for heur in heuristicas:
            puzzle = Puzzle15(estado_inicial)
            
            resultado = puzzle.a_estrella(heur)
            
            if resultado.get('exito', False):
                exito = "SI"
                profundidad = resultado['profundidad']
                nodos_gen = resultado['nodos_generados']
                nodos_exp = resultado['nodos_expandidos']
                tiempo = f"{resultado['tiempo']:.4f}"
            elif 'error' in resultado:
                exito = "NO"
                profundidad = "ERROR"
                nodos_gen = "-"
                nodos_exp = "-"
                tiempo = "-"
            else:
                exito = "NO"
                profundidad = "-"
                nodos_gen = resultado.get('nodos_generados', '-')
                nodos_exp = resultado.get('nodos_expandidos', '-')
                tiempo = f"{resultado.get('tiempo', 0):.4f}" if isinstance(resultado.get('tiempo', 0), (int, float)) else "-"
            
            print(f"{nombre_estado:<10} {heur:<15} {exito:<8} {str(profundidad):<12} {str(nodos_gen):<12} {str(nodos_exp):<12} {tiempo:<12}")

if __name__ == "__main__":
    print("\n" + "="*90)
    print("PRACTICA 2 - EJERCICIO 1".center(90))
    print("Comparativa de heuristicas para 8-puzzle y 15-puzzle".center(90))
    print("="*90)
    
    tabla_comparativa_8puzzle()
    tabla_comparativa_15puzzle()