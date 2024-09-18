import sys
import random
import time
import pygame

# INICIAR o PYGAME
def game_start(width, height):
    pygame.init()
    tamanho = width, height
    tela = pygame.display.set_mode(tamanho)
    pygame.display.set_caption("Apple Gravity")
    return tela

def create_apple(apples, apples_rect, timer, posicoes_usadas):
    apple = pygame.image.load("imgs/maca.png")
    apple = pygame.transform.scale(apple, (60, 70))
    apple_rect = apple.get_rect()

    positions = [(665, 50), (800, 123), (480, 123), (550, 115), (230, 115),
                 (265, 200), (430, 200), (835, 200), (900, 180), (160, 180),
                 (260, 280), (910, 280), (910, 330), (320, 330)]

    if len(posicoes_usadas) == len(positions):
        posicoes_usadas.clear() 
    if timer <= 45:
        
        while True:
            positions_aleatorio = random.randrange(len(positions))
            positions_rect = positions[positions_aleatorio]
            if positions_rect not in posicoes_usadas:
                posicoes_usadas.append(positions_rect)
                apple_rect.x, apple_rect.y = positions_rect
                break
    else:
        apple_rect.x = random.randrange(1020)
        apple_rect.y = -60

    apples.append(apple)
    apples_rect.append(apple_rect)

def create_pear(pears, pears_rect, timer, posicoes_usadas):
    pear = pygame.image.load("imgs/pera.png")
    pear = pygame.transform.scale(pear, (45, 55))
    pear_rect = pear.get_rect()

    positions = [(665, 50), (800, 123), (480, 123), (550, 115), (230, 115),
                 (265, 200), (430, 200), (835, 200), (900, 180), (160, 180),
                 (260, 280), (910, 280), (910, 330), (320, 330)]

    if len(posicoes_usadas) == len(positions):
        posicoes_usadas.clear()
    if 20 <= timer < 45:
       
        while True:
            positions_aleatorio = random.randrange(len(positions))
            positions_rect = positions[positions_aleatorio]
            if positions_rect not in posicoes_usadas:
                posicoes_usadas.append(positions_rect)
                pear_rect.x, pear_rect.y = positions_rect
                break
    elif timer >= 45:
        pear_rect.x = random.randrange(1020)
        pear_rect.y = -60

    pears.append(pear)
    pears_rect.append(pear_rect)

def draw_apples(apples, apples_rect, display):
    for i in range(len(apples)):
        display.blit(apples[i], apples_rect[i])

def draw_pears(pears, pears_rect, display, timer):
    if timer > 20:
        for i in range(len(pears)):
            display.blit(pears[i], pears_rect[i])

def draw_lifes(lifes_img,life_rect,display):
    for i in range(lifes):
        x = 6 + (i * 45)
        y = 10 
        display.blit(life_img, (x, y))

def capture_apples(apples, apples_rect, personagem_rect, score):
    new_apples = []
    new_apples_rect = []
    captured = False
    for i in range(len(apples)):
        x = apples_rect[i].x
        y = apples_rect[i].y
        crop = pygame.Rect((x, y), (25, 25))
        if personagem_rect.colliderect(crop):
            captured = True
            score += 1 
        else:
            new_apples.append(apples[i])
            new_apples_rect.append(apples_rect[i])
    return new_apples, new_apples_rect, captured, score

def capture_pears(pears, pears_rect, personagem_rect, storage):
    new_pears = []
    new_pears_rect = []
    captured = False
    for i in range(len(pears)):
        x = pears_rect[i].x
        y = pears_rect[i].y
        crop = pygame.Rect((x, y), (25, 25))
        if personagem_rect.colliderect(crop):
            captured = True
            storage += 1 
        else:
            new_pears.append(pears[i])
            new_pears_rect.append(pears_rect[i])
    return new_pears, new_pears_rect, captured, storage

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

# DEFINIÇÃO DOS PERSONAGENS
display = game_start(1080, 720)

bg_image = pygame.image.load("imgs/imagem_bg.jpg")
bg_image = pygame.transform.scale(bg_image, (1080, 720))

personagem = pygame.image.load("imgs/newton_posição_frente.png")
personagem = pygame.transform.scale(personagem, (140, 240))
personagem_rect = personagem.get_rect()
personagem_rect.x = 0
personagem_rect.y = 450

life_img = pygame.image.load("imgs/heart.png")
life_img = pygame.transform.scale(life_img, (40, 40)) 
life_rect = life_img.get_rect()

font = pygame.font.Font(None, 32)
text_color = (0,0,0)

# VARIAVEIS
lifes = 6
score = 0
storage = 0
cronometro = 0
last_update = pygame.time.get_ticks()
apple_speed = 2
current_frame = 0
personagem_speed = 6
distancia_para_nova_maca = 720
estado_de_jogo = "jogando"
posicoes_usadas = []  

apples = []
apples_rect = []
create_apple(apples, apples_rect, cronometro, posicoes_usadas)
apples_losts = 0
pears = []
pears_rect = []
create_pear(pears, pears_rect, cronometro, posicoes_usadas)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if estado_de_jogo == "jogando":
        personagem_rect = mover_player(keys, personagem_rect, personagem_speed)

        apple_speed, personagem_speed, distancia_para_nova_maca = temporizador(
            cronometro, apple_speed, personagem_speed, distancia_para_nova_maca
        )

        for i in range(len(apples_rect)):
            apples_rect[i].y += apple_speed
            if apples_rect[i].y > 725:
                apples_losts += 1
                apples.pop(i)  
                apples_rect.pop(i)  
                break  

        if cronometro > 20:
            for i in range(len(pears_rect)):
                pears_rect[i].y += apple_speed
                

        if len(apples_rect) > 0 and apples_rect[-1].y > distancia_para_nova_maca or apples_rect[-1].y > 720 :
            create_apple(apples, apples_rect, cronometro, posicoes_usadas)

        if len(pears_rect) > 0 and pears_rect[-1].y > distancia_para_nova_maca:
            create_pear(pears, pears_rect, cronometro, posicoes_usadas)

        apples, apples_rect, captured_apples, score = capture_apples(apples, apples_rect, personagem_rect, score)

        if captured_apples:
            create_apple(apples, apples_rect, cronometro, posicoes_usadas)

        pears, pears_rect, captured_pears, storage = capture_pears(pears, pears_rect, personagem_rect, storage)
        
        if captured_pears:
            create_pear(pears, pears_rect, cronometro, posicoes_usadas)

        if storage == 2:
            lifes = max(0, lifes - 1)
            storage = 0

        if apples_losts == 5:
            lifes = max(0, lifes - 1)
            apples_losts = 0
        

        display.blit(bg_image, (0, 0))
        draw_apples(apples, apples_rect, display)
        draw_pears(pears, pears_rect, display, cronometro)

        text = font.render("Score: " + str(score), True, text_color)
        display.blit(text, (10, 50))
        display.blit(personagem, personagem_rect)
        draw_lifes(life_img, lifes, display)
        if (pygame.time.get_ticks() - last_update) >= 1000:
            cronometro += 1
            last_update = pygame.time.get_ticks()
        if lifes == 0:
            estado_de_jogo = "fim_de_jogo"

        text2 = font.render("Time: " + str(cronometro) + "s", True, text_color)
        display.blit(text2, (10, 80))

    if estado_de_jogo == "fim_de_jogo":
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_r]:
            estado_de_jogo = "jogando"
            score = 0
            cronometro = 0
            last_update = pygame.time.get_ticks()

        display.blit(bg_image, (0, 0))
        text_fim = font.render(
            "Parabens, voce fez " + str(score) + " pontos", True, text_color
        )
        display.blit(text_fim, (350, 200))
        text_restart = font.render("Pressione R para reiniciar", True, text_color)
        display.blit(text_restart, (350, 300))
        text_quit = font.render("Pressione Q para sair", True, text_color)
        display.blit(text_quit, (350, 350))
    print(apples_losts)
    pygame.display.flip()
    time.sleep(0.015)
