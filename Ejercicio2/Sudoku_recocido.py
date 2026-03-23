import pygame
import random
import sys
import time
import tracemalloc
import math

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
WINDOW_SIZE = (540, 620)
CELL_SIZE = 540 // 9
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("SUDOKU IA - Recocido Simulado")

# Colores y Fuentes
WHITE, BLACK, BLUE, RED = (255, 255, 255), (0, 0, 0), (0, 0, 255), (200, 0, 0)
font_num = pygame.font.SysFont("calibri", 40, bold=True)
font_ui = pygame.font.SysFont("calibri", 20)

# ---------------- IA ----------------

def initial_solution(grid):
    #Copia el tablero original
    new_grid = [row[:] for row in grid]
    
    for i in range(9):
        nums = list(range(1, 10))
        random.shuffle(nums)  # Copia el tablero original
        
        for j in range(9):
            if new_grid[i][j] == 0:  # Si la celda esta vacia, pasa a la instruccion de abajo
                new_grid[i][j] = nums.pop() # Donde a la celda vacia, se le asigna un nuevo aleatorio
    
    return new_grid  # Regresa el tablero ya resuelto , aunque esten mal algunos numeros


def cost(grid): #Calcula el numero de errores en el Sudoku
    errores = 0
    
    # filas
    for row in grid:
        errores += 9 - len(set(row)) #set(row) sirve para eliminar duplicados, osea cuenta cuantos numeros repetidos hay en la fila
    
    # columnas
    for col in zip(*grid): #Convierte filas en columnas 
        errores += 9 - len(set(col)) #Cuenta cuantos numeros repetidos hay en las columnas ,  9 - (Numeros unicos)
    
    return errores #Entre menor sea el numeros de errores, mejor solucion


def get_neighbor(grid, fixed):
    new_grid = [row[:] for row in grid]
    
    #Selecciona un subcuadro 3*3 
    box_row = random.randint(0, 2) * 3 
    box_col = random.randint(0, 2) * 3 
    
    cells = []
    for i in range(3):
        for j in range(3):
            r, c = box_row + i, box_col + j #Recorres las posiciones dentro del subcuadro 3x3
            if not fixed[r][c]: #si NO es fija (se puede cambiar)
                cells.append((r, c)) #Guarda las posiciones de las celdas modificables 
    
    if len(cells) >= 2:
        a, b = random.sample(cells, 2) #Elige 2 posiciones aleatorias distintas
        new_grid[a[0]][a[1]], new_grid[b[0]][b[1]] = new_grid[b[0]][b[1]], new_grid[a[0]][a[1]] #Intercambia los valores 
    
    return new_grid ## Devuelve un tablero ligeramente modificado


def simulated_annealing(grid, max_iter=20000, temp=1.0, cooling=0.995):#Parametros (grid-- tablero original,max_iter--Numero maximo de iteraciones, temp-- temperatura inicial, valor de enfriamiento
    
    fixed = [[grid[r][c] != 0 for c in range(9)] for r in range(9)] # Matriz que indica qué celdas son fijas (True) y cuáles se pueden modificar (False)
    
    current = initial_solution(grid) #Genera una solucion inicial  aleatoria (aunque no este correcta)
    current_cost = cost(current) # Calcula el número de errores de la solución actual
    
    #Guarda la mejor solucion encontrada
    best = current 
    best_cost = current_cost

    for _ in range(max_iter): 
        candidate = get_neighbor(current, fixed) #Genera una nueva solucion  vecina a partir de la actual 
        candidate_cost = cost(candidate) # Calcula el costo (número de errores) de la solución candidata
        
        diff = candidate_cost - current_cost # Calcula la diferencia entre el costo nuevo y el actual
        

        # Se acepta la nueva solución si:
        # 1. Es mejor (menos errores)
        # 2. O, aunque sea peor, se acepta con cierta probabilidad
        if diff < 0 or random.random() < math.exp(-diff / temp): #Escapa de soluciones malas locales
            current = candidate #Actualiza la solucion mejor   
            current_cost = candidate_cost  #Actualiza el costo de la nueva solucion 
            
            if candidate_cost < best_cost: # Si es la mejor encontrada hasta ahora, entonces:
                best = candidate # Guarda esta solución como la mejor
                best_cost = candidate_cost #Guarda su costo
        
        temp *= cooling  # Reduce la temperatura (enfriamiento)
        
        if best_cost == 0:  # Si ya no hay errores (solución perfecta)
            break  # Termina antes del límite de iteraciones
    
    return best


# ----------- GENERACIÓN -----------

def generate_sudoku(empty_cells):
    grid = [[0 for _ in range(9)] for _ in range(9)]
    
    # Genera solución completa primero
    solution = simulated_annealing(grid)
    
    # Quita números
    for _ in range(empty_cells):
        r, c = random.randint(0, 8), random.randint(0, 8)
        solution[r][c] = 0
    
    return solution


# ----------- DIBUJO -----------

def draw_all(grid, msg):
    screen.fill(WHITE)

    # líneas
    for i in range(10):
        thick = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (540, i * CELL_SIZE), thick)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, 540), thick)

    # números
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                val = font_num.render(str(grid[r][c]), True, BLACK)
                screen.blit(val, (c * CELL_SIZE + 20, r * CELL_SIZE + 10))

    txt = font_ui.render(msg, True, BLUE)
    screen.blit(txt, (20, 560))

    instr = font_ui.render("1,2,3: Dificultad | ESPACIO: Resolver (Recocido)", True, RED)
    screen.blit(instr, (20, 585))


# ----------- MAIN -----------

def main():
    grid = generate_sudoku(35)
    msg = "Nivel: Intermedio"

    while True:
        draw_all(grid, msg)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    grid = generate_sudoku(20)
                    msg = "Nivel: Fácil"

                if event.key == pygame.K_2:
                    grid = generate_sudoku(35)
                    msg = "Nivel: Intermedio"

                if event.key == pygame.K_3:
                    grid = generate_sudoku(45)
                    msg = "Nivel: Difícil"

                if event.key == pygame.K_SPACE:
                    tracemalloc.start()
                    start_time = time.time()

                    grid = simulated_annealing(grid)

                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    elapsed_time = end_time - start_time
                    msg = f"Tiempo: {elapsed_time:.4f}s | Mem: {peak/10**6:.4f}MB"

        pygame.display.flip()


if __name__ == "__main__":
    main()