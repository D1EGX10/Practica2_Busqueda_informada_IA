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
    new_grid = [row[:] for row in grid]
    
    for i in range(9):
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for j in range(9):
            if new_grid[i][j] == 0:
                new_grid[i][j] = nums.pop()
    
    return new_grid


def cost(grid):
    errores = 0
    
    # filas
    for row in grid:
        errores += 9 - len(set(row))
    
    # columnas
    for col in zip(*grid):
        errores += 9 - len(set(col))
    
    return errores


def get_neighbor(grid, fixed):
    new_grid = [row[:] for row in grid]
    
    box_row = random.randint(0, 2) * 3
    box_col = random.randint(0, 2) * 3
    
    cells = []
    for i in range(3):
        for j in range(3):
            r, c = box_row + i, box_col + j
            if not fixed[r][c]:
                cells.append((r, c))
    
    if len(cells) >= 2:
        a, b = random.sample(cells, 2)
        new_grid[a[0]][a[1]], new_grid[b[0]][b[1]] = new_grid[b[0]][b[1]], new_grid[a[0]][a[1]]
    
    return new_grid


def simulated_annealing(grid, max_iter=20000, temp=1.0, cooling=0.995):
    
    fixed = [[grid[r][c] != 0 for c in range(9)] for r in range(9)]
    
    current = initial_solution(grid)
    current_cost = cost(current)
    
    best = current
    best_cost = current_cost

    for _ in range(max_iter):
        candidate = get_neighbor(current, fixed)
        candidate_cost = cost(candidate)
        
        diff = candidate_cost - current_cost
        
        if diff < 0 or random.random() < math.exp(-diff / temp):
            current = candidate
            current_cost = candidate_cost
            
            if candidate_cost < best_cost:
                best = candidate
                best_cost = candidate_cost
        
        temp *= cooling
        
        if best_cost == 0:
            break
    
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