
import random
import pygame

pygame.init() #Inicialización de la libreria pygame
 
#Valores de los colores a utilizar en el sudoku
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)

#Tamaño de la ventaja del juego 

WINDOW_SIZE = (550, 550)
CELL_SIZE = WINDOW_SIZE[0] // 9


pygame.display.set_caption("SUDOKU") #Titulo del juego

screen = pygame.display.set_mode(WINDOW_SIZE) #Crear la ventaja del juego

#FTipo de letra a utilizar
font_large = pygame.font.SysFont("calibri", 50)
font_small = pygame.font.SysFont("calibri", 30)

#Generar la cuadricula del sudoku
def generate_sudoku(difficulty):

## Llenar las subcuadrículas diagonales
for i in range(0, 9, 3):
    nums = random.sample(range(1, 10), 3)
    for j in range(3):
        grid[i + j][i + j] = nums[j]

## Elimina números según el nivel de dificultad
num_to_remove = 45 + 10 * difficulty
for _ in range(num_to_remove):
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    grid[row][col] = 0

return grid

    pass

#Resolver las cuadriculas del sudoku
def solve_sudoku(grid):
   #Devuelve las coordenas de la celda vacia en la cuadricula 
   def find_empty_cell(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)

    return None
   
   ## Intenta llenar la celda vacía con números del 1 al 9
for num in range(1, 10):
    if is_valid_move(grid, row, col, num):
        grid[row][col] = num

        if solve_sudoku(grid):
            return True

        ## Si el número actual conduce a una solución no válida, retrocede
        grid[row][col] = 0

return False
   
   #Valida si el numero colocado es valido
   def is_valid_move(grid, row, col, num):
    ## Código de la función va aquí
    pass
   
    pass

def draw_grid(grid, selected_cell):
    ## Código de la función va aquí
    pass

