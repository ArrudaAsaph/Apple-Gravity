import sys
import random
import time
import pygame


# INICIAR o PYGAME
def game_start(width,height):
    pygame.init()
    tamanho = width , height
    tela = pygame.display.set_mode(tamanho)
    pygame.display.set_caption("Apple Gravity")
    return tela

def create_apple(apples,apples_rect,timer):

    apple = pygame.image.load("testes/maca.png")
    apple = pygame.transform.scale(apple, (60, 70))
    apple_rect = apple.get_rect()

    if timer <= 45:
        positions = [(665, 50), (800, 123), (480, 123), (550, 115), (230, 115), 
                (265, 200), (430, 200), (835, 200), (900, 180), (160, 180), 
                (260, 280), (910, 280), (910, 330), (320, 330)]
        
        positions_aleatorio = random.randrange(14)
        positions_rect = positions[positions_aleatorio]
        apple_rect.x , apple_rect.y = positions_rect
        
    else:
        apple_rect.x  = random.randrange(1020)
        apple_rect.y  = -60

    apples.append(apple)
    apples_rect.append(apple_rect)

def draw_apples(apples, apples_rect, display):
    for i in range(len(apples)):
        display.blit(apples[i], apples_rect[i])

def capture_apples(apples, apples_rect, personagem_rect):
    new_apples = []
    new_apples_rect = []
    captured = False
    for i in range(len(apples)):
        x = apples_rect[i].x
        y = apples_rect[i].y
        crop = pygame.Rect((x, y), (25, 25))
        if personagem_rect.colliderect(crop):
            captured = True
        else:
            new_apples.append(apples[i])
            new_apples_rect.append(apples_rect[i])
    return new_apples, new_apples_rect, captured

def mover_player(keys, personagem_rect, speed):
    if keys[pygame.K_LEFT]:
        personagem_rect.x -= speed
        if personagem_rect.left < 0:
            personagem_rect.left = 0
    if keys[pygame.K_RIGHT]:
        personagem_rect.x += speed
        if personagem_rect.right > 1080:
            personagem_rect.right = 1080
    return personagem_rect

def temporizador(cronometro, apple_speed, personagem_speed, distancia):
    if 10 < cronometro < 20:
        apple_speed = 2.5
        personagem_speed = 6.2
    elif 20 < cronometro < 30:
        apple_speed = 3
        personagem_speed = 6.5
        distancia = 600
    elif 30 < cronometro < 38:
        apple_speed = 4.5
        personagem_speed = 7
        distancia = 500
    elif 38 < cronometro < 50:
        apple_speed = 5
        personagem_speed = 7.2
        distancia = 450
    elif cronometro > 50:
        apple_speed = 5.5
        personagem_speed = 7.8
        distancia = 400
    return apple_speed, personagem_speed, distancia

# def walking(keys, personagem_rect, frames, current_frame, last_update, frame_rate):
    if keys[pygame.K_RIGHT]:  # Verifica se o jogador está andando para a direita
        now = pygame.time.get_ticks()
        if now - last_update > frame_rate:  # Controle da troca de frame por tempo
            last_update = now
            current_frame = (current_frame + 1) % len(frames)  # Alterna entre os frames
        personagem = pygame.image.load(frames[current_frame])
        personagem = pygame.transform.scale(personagem, (142, 247))
    else:
        # Se não estiver andando, mantém o personagem parado
        personagem = pygame.image.load("testes/newton_posição_frente.png")
        personagem = pygame.transform.scale(personagem, (142, 247))
    return personagem, current_frame, last_update


# DEFINIÇÃO DOS PERSONAGENS
display = game_start(1080, 720)

bg_image = pygame.image.load("testes/imagem_bg.jpg")
bg_image = pygame.transform.scale(bg_image, (1080, 720))

personagem = pygame.image.load("testes/newton_posição_frente.png")
personagem = pygame.transform.scale(personagem, (140,240))
personagem_rect = personagem.get_rect()
personagem_rect.x = 0
personagem_rect.y = 450  





# VARIAVEIS
cronometro = 0
last_update = pygame.time.get_ticks()
apple_speed = 2
current_frame = 0
personagem_speed = 6
distancia_para_nova_maca = 720

apples = []
apples_rect = []
create_apple(apples, apples_rect, cronometro)


while True:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    personagem_rect = mover_player(keys, personagem_rect, personagem_speed)

    apple_speed, personagem_speed, distancia_para_nova_maca = temporizador(
        cronometro, apple_speed, personagem_speed, distancia_para_nova_maca
    )

    
    for i in range(len(apples_rect)):
        apples_rect[i].y += apple_speed

    
    if len(apples_rect) > 0 and apples_rect[-1].y > distancia_para_nova_maca:
        create_apple(apples, apples_rect, cronometro)

    
    apples, apples_rect, captured = capture_apples(apples, apples_rect, personagem_rect)

    
    if captured:
        create_apple(apples, apples_rect, cronometro)

    
    if (pygame.time.get_ticks() - last_update) >= 1000:
        cronometro += 1
        last_update = pygame.time.get_ticks()


    display.blit(bg_image, (0, 0))
    draw_apples(apples, apples_rect, display)
    display.blit(personagem, personagem_rect)

    pygame.display.flip()
    time.sleep(0.015)
