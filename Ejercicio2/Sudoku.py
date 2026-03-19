import pygame
import random
import sys

# Inicialización
pygame.init()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Configuración básica
WINDOW_SIZE = (540, 600) # 60px extra abajo para el menú
CELL_SIZE = 540 // 9
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("SUDOKU - IA")

# Fuentes
font_large = pygame.font.SysFont("calibri", 40, bold=True)
font_small = pygame.font.SysFont("calibri", 25)

def is_valid_move(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False
    return True

def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums) # Para que cada Sudoku sea diferente
                for num in nums:
                    if is_valid_move(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def generate_sudoku(empty_cells):
    grid = [[0 for _ in range(9)] for _ in range(9)]
    solve_sudoku(grid) 
    
    count = empty_cells
    while count > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            count -= 1
    return grid

# --- NUEVAS FUNCIONES DE DIBUJO ---

def draw_grid():
    for i in range(10):
        # Líneas más gruesas para separar los bloques de 3x3
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (540, i * CELL_SIZE), thickness)
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, 540), thickness)

def draw_numbers(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] != 0:
                text = font_large.render(str(grid[row][col]), True, BLACK)
                # Centrar el número en la celda
                screen.blit(text, (col * CELL_SIZE + 20, row * CELL_SIZE + 10))

def main():
    difficulty_text = "Nivel: Intermedio (35)"
    grid = generate_sudoku(35)
    running = True
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Detectar teclas para dificultad
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    grid = generate_sudoku(20)
                    difficulty_text = "Nivel: Fácil (20)"
                if event.key == pygame.K_2:
                    grid = generate_sudoku(35)
                    difficulty_text = "Nivel: Intermedio (35)"
                if event.key == pygame.K_3:
                    grid = generate_sudoku(45)
                    difficulty_text = "Nivel: Difícil (45)"
        
        # Dibujar elementos
        draw_grid()
        draw_numbers(grid)
        
        # Dibujar menú de instrucciones abajo
        info = font_small.render(difficulty_text, True, BLUE)
        menu = font_small.render("Presiona 1, 2 o 3 para cambiar nivel", True, BLACK)
        screen.blit(info, (10, 545))
        screen.blit(menu, (10, 570))
        
        pygame.display.flip()

if __name__ == "__main__":
    main()