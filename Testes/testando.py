import pygame
import random

# Inicializa o Pygame
pygame.init()

# Define as dimensões da tela
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define as cores
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Define os parâmetros dos quadrados
square_size = 50
fall_speed = 3  # Velocidade de queda dos quadrados

# Carrega a imagem do coração e define a cor de fundo como transparente
heart_img = pygame.image.load("heart.png")  # Certifique-se de ter uma imagem de coração chamada 'heart.png'
heart_img = pygame.transform.scale(heart_img, (40, 40))  # Redimensiona para o tamanho desejado

# Define a cor que será transparente
heart_img.set_colorkey(WHITE)  # A cor branca na imagem será transparente

# Número inicial de vidas
lives = 3
heart_width = 40
heart_height = 40

# Função para criar um novo quadrado no topo da tela
def create_square():
    x_position = random.randint(0, screen_width - square_size)
    return pygame.Rect(x_position, 0, square_size, square_size)

# Função para desenhar vidas (corações) com preenchimento vermelho para a vida restante
def draw_lives(screen, lives):
    for i in range(lives):
        x = 10 + i * 45
        y = 10
        
        # Desenha a parte do coração preenchida
        # Cria uma superfície vermelha para sobrepor a imagem do coração
        heart_fill = pygame.Surface((heart_width, heart_height))
        heart_fill.fill(RED)
        heart_fill.set_colorkey(RED)
        
        screen.blit(heart_fill, (x, y))  # Desenha o fundo vermelho
        screen.blit(heart_img, (x, y))  # Desenha a imagem do coração sobre o fundo vermelho

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

    # Verifica se algum quadrado saiu da tela e reduz vida
    for square in squares[:]:  # Itera sobre uma cópia da lista
        if square.y > screen_height:
            squares.remove(square)  # Remove o quadrado da lista
            lives = max(0, lives - 1)  # Perde 50% da vida de cada coração

    # Verifica se o jogador perdeu todas as vidas
    if lives <= 0:
        running = False  # Finaliza o jogo quando não houver mais vidas

    # Remove quadrados que saíram da tela
    squares = [square for square in squares if square.y <= screen_height]

    # Desenha os quadrados
    for square in squares:
        pygame.draw.rect(screen, RED, square)

    # Desenha os corações na tela
    draw_lives(screen, lives)

    pygame.display.flip()  # Atualiza a tela
    clock.tick(60)  # Controla a taxa de quadros por segundo

# Finaliza o Pygame
pygame.quit()
