import pygame
import random
import sys

# --- CONFIGURACIÓN INICIAL ---
pygame.init()
WINDOW_SIZE = (540, 620)
CELL_SIZE = 540 // 9
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("SUDOKU IA - Algoritmo A*")

# Colores y Fuentes
WHITE, BLACK, BLUE, RED = (255, 255, 255), (0, 0, 0), (0, 0, 255), (200, 0, 0)
font_num = pygame.font.SysFont("calibri", 40, bold=True)
font_ui = pygame.font.SysFont("calibri", 20)

# --- LÓGICA DE IA ---

def is_valid_move(grid, row, col, num):  #Define si el movimiento que se hizo es correcto
    for x in range(9):  #Escogie los numeros del a al 9
        if grid[row][x] == num or grid[x][col] == num:  #Se desplaza ya sea por columna o por fila, para saber si el numero es igual en alguna de esas posiciones 
            return False #Regresa que el numero no es valido 

    start_r, start_c = 3 * (row // 3), 3 * (col // 3) # Calcula la posición inicial del subcuadro 3x3 correspondiente
    for i in range(3):
        for j in range(3):  # Recorre el subcuadro 3x3
            if grid[start_r + i][start_c + j] == num: #Busca que el numero no coincida con alguno en el recuadro
                return False
    return True

def get_mrv_cell(grid): #Busca la celda vacía que tenga menos opciones posibles.
    """ Heurística MRV: Busca la celda con menos opciones legales """
    best_cell = None # Guarda la mejor celda encontrada (fila, columna)
    min_options = 10  # Máximos posible es de 9, usamos 10 como valor inicial "grande"
    
    for r in range(9): # Recorre filas
        for c in range(9):  # Recorre columnas
            if grid[r][c] == 0: #Busca celdas vacias 
                # Contamos cuántas opciones tiene esta celda
                options = sum(1 for n in range(1, 10) if is_valid_move(grid, r, c, n)) # Cuántos números (1–9) se pueden poner en esa celda
                if options < min_options: #Busca la celda con MENOS opciones disponibles
                    min_options = options #Guarda el nuevo mínimo
                    best_cell = (r, c) #Guarda la posición de esa celda
                if min_options == 1: return best_cell # Si solo hay 1 opción, es la mejor
    return best_cell

def solve_astar(grid):
    """ Implementación de A* usando la heurística MRV """
    cell = get_mrv_cell(grid)  # Obtiene la celda vacía con menos opciones posibles
    if not cell: return True # No hay más celdas vacías
    
    row, col = cell  # Obtiene las coordenadas de la celda seleccionada
    for num in range(1, 10):  # Prueba números del 1 al 9
        if is_valid_move(grid, row, col, num):     # Verifica si el número es válido en esa posición
            grid[row][col] = num  # Asigna temporalmente el número a la celda

            
            # Llamada recursiva (Búsqueda en el espacio de estados)
            if solve_astar(grid):
                return True
            
            grid[row][col] = 0  # Backtracking: deshace el movimiento si no funcionó
    return False

# --- FUNCIONES DE DIBUJO ---

def generate_sudoku(empty_cells):
    grid = [[0 for _ in range(9)] for _ in range(9)]
    # Usamos A* para generar un tablero válido inicial
    solve_astar(grid)
    for _ in range(empty_cells):
        r, c = random.randint(0, 8), random.randint(0, 8)
        while grid[r][c] == 0: r, c = random.randint(0, 8), random.randint(0, 8)
        grid[r][c] = 0
    return grid

def draw_all(grid, msg):
    screen.fill(WHITE)
    # Dibujar líneas
    for i in range(10):
        thick = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (540, i * CELL_SIZE), thick)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, 540), thick)
    # Dibujar números
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                val = font_num.render(str(grid[r][c]), True, BLACK)
                screen.blit(val, (c * CELL_SIZE + 20, r * CELL_SIZE + 10))
    # UI
    txt = font_ui.render(msg, True, BLUE)
    screen.blit(txt, (20, 560))
    instr = font_ui.render("1,2,3: Dificultad | ESPACIO: IA Resuelve (A*)", True, RED)
    screen.blit(instr, (20, 585))

# --- BUCLE PRINCIPAL ---

def main():
    grid = generate_sudoku(35)
    msg = "Nivel: Intermedio"
    
    while True:
        draw_all(grid, msg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    grid = generate_sudoku(20); msg = "Nivel: Fácil"
                if event.key == pygame.K_2: 
                    grid = generate_sudoku(35); msg = "Nivel: Intermedio"
                if event.key == pygame.K_3: 
                    grid = generate_sudoku(45); msg = "Nivel: Difícil"
                if event.key == pygame.K_SPACE:
                    solve_astar(grid) # Ejecutar A*
        
        pygame.display.flip()

if __name__ == "__main__":
    main()