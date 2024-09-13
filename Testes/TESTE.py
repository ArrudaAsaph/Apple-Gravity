import sys
import random
import time
import pygame


# INICIAR O JOGO
def game_start(w, h):
    pygame.init()
    tamanho = w, h
    tela = pygame.display.set_mode(tamanho)
    pygame.display.set_caption("Apple Newton")
    return tela


# CRIAR AS MAÇAS
def create_apple(apples, apples_rect):
    ranges = [(665, 50), (800, 123), (480, 123), (550, 115), (230, 115), 
              (265, 200), (430, 200), (835, 200), (900, 180), (160, 180), 
              (260, 280), (910, 280), (910, 330), (320, 330)]
    apple = pygame.image.load("testes/maca.png")
    apple = pygame.transform.scale(apple, (60, 70))
    apple_rect = apple.get_rect()
    n_aleatorio = random.randrange(14)
    teste = ranges[n_aleatorio]
    apple_rect.x, apple_rect.y = teste
    apples.append(apple)
    apples_rect.append(apple_rect)


# DESENHAR AS MAÇAS
def draw_apples(apples, apples_rect, display):
    for i in range(len(apples)):
        display.blit(apples[i], apples_rect[i])


# CAPTURAR AS MAÇAS
def capture_apples(apples, apples_rect, personagem_rect):
    new_apples = []
    new_apples_rect = []
    captured = False  # Variável para detectar captura
    for i in range(0, len(apples)):
        x = apples_rect[i].x
        y = apples_rect[i].y
        crop = pygame.Rect((x, y), (25, 25))  # Área de captura
        if personagem_rect.colliderect(crop):
            captured = True  # Maçã foi capturada
        else:
            new_apples.append(apples[i])
            new_apples_rect.append(apples_rect[i])

    return new_apples, new_apples_rect, captured

# Função para mover o jogador
def mover_player(keys, personagem_rect, speed):
    if keys[pygame.K_LEFT]:
        personagem_rect.x -= speed
        if personagem_rect.left < -30:
            personagem_rect.left = -30
    if keys[pygame.K_RIGHT]:
        personagem_rect.x += speed
        if personagem_rect.right > 1200:
            personagem_rect.right = 1200
    return personagem_rect

def temporizador(cronometro, apple_speed,personagem_speed,distancia):
    if cronometro > 10 and  cronometro < 20:
        apple_speed = 2.5
        personagem_speed = 6.2
    elif cronometro > 20 and cronometro < 30:
        apple_speed = 3
        personagem_speed = 6.5
        distancia = 600
    elif cronometro > 30 and cronometro <38:
        apple_speed = 4.5
        personagem_speed = 7
        distancia = 500
    elif cronometro > 38 and cronometro <50:
        apple_speed = 5
        personagem_speed = 7.2
        distancia = 450
    elif cronometro > 50:
        apple_speed = 5.5
        personagem_speed = 7.8
        distancia = 400
    return apple_speed, personagem_speed,distancia


# Inicializar o display do jogo
display = game_start(1080, 720)

# Criar as maçãs
apples = []
apples_rect = []
create_apple(apples, apples_rect)  # Criamos a primeira maçã

# Imagem de fundo e personagem
bg_image = pygame.image.load("testes/imagem_bg.jpg")
bg_image = pygame.transform.scale(bg_image, (1080, 720))

personagem = pygame.image.load("testes/boneco_newton.png")
personagem_rect = personagem.get_rect()
personagem_rect.x = -30
personagem_rect.y = 520

# Variáveis de controle
sec = 0
t = pygame.time.get_ticks()


apple_speed = 2
personagem_speed = 6
distancia_para_nova_maca = 720 # Defina a distância para iniciar a queda de outra maçã
cronometro = 0

# Loop principal do jogo
while True:
    # Eventos do Pygame (sair do jogo)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controles do personagem
    keys = pygame.key.get_pressed()
    personagem_rect = mover_player(keys, personagem_rect, personagem_speed)
    apple_speed, personagem_speed, distancia_para_nova_maca = temporizador(cronometro ,apple_speed,personagem_speed,distancia_para_nova_maca)

    # Mover as maçãs atuais para baixo
    for i in range(len(apples_rect)):
        apples_rect[i].y += apple_speed

    # Verificar se a maçã mais recente passou da distância definida e criar uma nova
    if len(apples_rect) > 0 and apples_rect[-1].y > distancia_para_nova_maca:
        create_apple(apples, apples_rect)

    # Verificar se o personagem capturou alguma maçã
    apples, apples_rect, captured = capture_apples(apples, apples_rect, personagem_rect)

    # Se uma maçã foi capturada, criar uma nova
    if captured:
        create_apple(apples, apples_rect)


    if (pygame.time.get_ticks() - t) >= 1000:
            cronometro += 1
            t = pygame.time.get_ticks()


    # Desenhar fundo e todos os objetos
    display.blit(bg_image, (0, 0))
    draw_apples(apples, apples_rect, display)
    display.blit(personagem, personagem_rect)
    print(cronometro)

    pygame.display.flip()
    time.sleep(0.015)
