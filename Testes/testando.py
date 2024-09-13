import pygame
import random

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define a cor do quadrado
RED = (255, 0, 0)

# Define os parâmetros dos quadrados
square_size = 50
fall_speed = 3  # Velocidade de queda dos quadrados

# Função para criar um novo quadrado no topo da tela
def create_square():
    x_position = random.randint(0, screen_width - square_size)
    return pygame.Rect(x_position, 0, square_size, square_size)

# Lista de quadrados
squares = [create_square()]

# Controle de loop principal
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Limpa a tela com fundo preto

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimentação e spawn dos quadrados
    for square in squares:
        square.y += fall_speed  # Move o quadrado para baixo

    # Se o quadrado atingir o meio da tela, cria outro quadrado no topo
    if len(squares) == 1 and squares[0].y > screen_height // 2:
        squares.append(create_square())

    if len(squares) == 2 and all(square.y > screen_height for square in squares):
        squares.append(create_square())

    # Remove quadrados que saíram da tela
    squares = [square for square in squares if square.y <= screen_height]

    # Desenha os quadrados
    for square in squares:
        pygame.draw.rect(screen, RED, square)

    pygame.display.flip()  # Atualiza a tela
    clock.tick(60)  # Controla a taxa de quadros por segundo

# Finaliza o Pygame
pygame.quit()
