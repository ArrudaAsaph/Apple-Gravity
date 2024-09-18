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
    apple = pygame.image.load("testes/maca.png")
    apple = pygame.transform.scale(apple, (60, 70))
    apple_rect = apple.get_rect()

    positions = [(665, 50), (800, 123), (480, 123), (550, 115), (230, 115),
                 (265, 200), (430, 200), (835, 200), (900, 180), (160, 180),
                 (260, 280), (910, 280), (910, 330), (320, 330)]

    if len(posicoes_usadas) == len(positions):
        posicoes_usadas.clear()  # Limpar a lista se todas as posições tiverem sido usadas

    if timer <= 45:
        # Garantir que a posição não se repita
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
    pear = pygame.image.load("testes/pera.png")
    pear = pygame.transform.scale(pear, (45, 55))
    pear_rect = pear.get_rect()

    positions = [(665, 50), (800, 123), (480, 123), (550, 115), (230, 115),
                 (265, 200), (430, 200), (835, 200), (900, 180), (160, 180),
                 (260, 280), (910, 280), (910, 330), (320, 330)]

    if len(posicoes_usadas) == len(positions):
        posicoes_usadas.clear()  # Limpar a lista se todas as posições tiverem sido usadas

    if 20 <= timer < 45:
        # Garantir que a pera use uma posição válida da árvore
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

def create_golden_apple(apples_golden, apples_golden_rect,condicao_queda):
    if condicao_queda == True:
        apple_golden = pygame.image.load("testes/maca_dourada_bonus.png")
        apple_golden = pygame.transform.scale(apple_golden, (30, 40))
        apple_golden_rect = apple_golden.get_rect()
        apple_golden_rect.x = random.randrange(1020)
        apple_golden_rect.y = -60
        apples_golden.append(apple_golden)
        apples_golden_rect.append(apple_golden_rect)
    
def draw_apple_golden(apples_golden, apples_golden_rect, display):
    for i in range(len(apples_golden)):
        display.blit(apples_golden[i], apples_golden_rect[i])

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

def capture_apples(apples, apples_rect, personagem_rect, score,restart_apples):
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
            restart_apples += 1 
        else:
            new_apples.append(apples[i])
            new_apples_rect.append(apples_rect[i])
    return new_apples, new_apples_rect, captured, score,restart_apples

def capture_apples_golden(apples_golden, apples_golden_rect, personagem_rect, lifes,score,apple_golden_cont):
    new_apples_golden = []
    new_apples_golden_rect = []
    captured = False
    for i in range(len(apples_golden)):
        x = apples_golden_rect[i].x
        y = apples_golden_rect[i].y
        crop = pygame.Rect((x, y), (25, 25))
        if personagem_rect.colliderect(crop):
            captured = True 
            score += 20
            apple_golden_cont += 1
            if lifes in range(1,4):
                lifes +=3
            else:
                lifes = 6
        else:
            new_apples_golden.append(apples_golden[i])
            new_apples_golden_rect.append(apples_golden_rect[i])
    return new_apples_golden, new_apples_golden_rect, captured, lifes,score,apple_golden_cont

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

def temporizador_maca(cronometro, apple_speed, personagem_speed, distancia):
    if 10 < cronometro < 20:
        apple_speed = 2.8
        personagem_speed = 6.2
    elif 20 < cronometro < 30:
        apple_speed = 3.4
        personagem_speed = 6.8
        distancia = 600
    elif 30 < cronometro < 38:
        apple_speed = 4.5
        personagem_speed = 7
        distancia = 500
    elif 38 < cronometro < 50:
        apple_speed = 5
        personagem_speed = 7.2
        distancia = 450
    elif cronometro > 45:
        apple_speed = 5.5
        personagem_speed = 8.3
        distancia = 20
    return apple_speed, personagem_speed, distancia

def temporizador_pera(cronometro, pear_speed, distancia):
    if 20 < cronometro < 28:
        pear_speed = 2.4
    elif 28 < cronometro < 41:
        pear_speed = 3.5
        personagem_speed = 7
        distancia = 420
    elif 41 < cronometro < 50:
        pear_speed = 4.5
        distancia = 450
    elif cronometro > 45:
        pear_speed = 5.2
        distancia = 120
    return pear_speed, distancia

def lifes_controls(lifes,estado_de_jogo,storage,apples_losts,restart_apples,timer):
    if lifes == 0:
        estado_de_jogo = "fim_de_jogo"
        lifes = 6
        storage = 0
        apples_losts = 0
        timer = 0
    if storage == 2:
            lifes = max(0, lifes - 1)
            storage = 0
            restart_apples = 0
    if apples_losts == 10:
            lifes = max(0, lifes - 1)
            apples_losts = 0
            restart_apples = 0
    if lifes <6 and restart_apples == 10:
        lifes += 1
        restart_apples = 0

    if timer > 60:
        if restart_apples > 4:
            apples_losts = 0
    return lifes,estado_de_jogo,storage,apples_losts,restart_apples,timer

def cair_apples(apples,apples_rect,apple_speed,apples_lost,distancia_para_nova_maca):
    for i in range(len(apples_rect)):
        apples_rect[i].y += apple_speed
        if apples_rect[i].y > 725:
            apples_lost += 1
            apples.pop(i)
            apples_rect.pop(i)
            break
    if len(apples_rect) >= 0 and apples_rect[-1].y > distancia_para_nova_maca or apples_rect[-1].y > 720 :
        create_apple(apples, apples_rect, cronometro, posicoes_usadas)
    return apples , apples_rect , apples_lost

def cair_apples_golden(apples_golden, apples_golden_rect, apple_speed, condicao_queda, lifes, timer,apple_golden_cont):
    # Only trigger the golden apple spawn condition after 10 seconds and when lifes are 4 or less
    if timer > 60 and lifes < 2 and not condicao_queda:
        condicao_queda = True
        create_golden_apple(apples_golden, apples_golden_rect, condicao_queda)

    # Move the golden apple if it exists
    for i in range(len(apples_golden_rect)):
        apples_golden_rect[i].y += apple_speed
        if apples_golden_rect[i].y > 725:  # If the golden apple goes off-screen
            apples_golden.pop(i)
            apples_golden_rect.pop(i)
            break

    return apples_golden, apples_golden_rect, condicao_queda

def cair_pears(pears,pears_rect,pear_speed,timer,distancia_para_nova_maca):
    if (timer == 10):
        pears_rect[0].x = 665
        pears_rect[0].y = 50
        while pears_rect[0].y < 720:
            pears_rect[0].y += pear_speed
    elif (timer > 20):
        for i in range(len(pears_rect)):
                pears_rect[i].y += apple_speed 
        if len(pears_rect) > 0 and pears_rect[-1].y > distancia_para_nova_maca:
            create_pear(pears, pears_rect, cronometro, posicoes_usadas)          
    return pears , pears_rect

def create_albert(alberts, alberts_rect, timer, albert_active):
    if timer > 85 and not albert_active:
        albert = pygame.image.load("testes/boneco_albert.png")
        albert = pygame.transform.scale(albert, (80, 80))
        albert_rect = albert.get_rect()
        albert_rect.x = 1300  # Posição inicial do Albert fora da tela (à direita)
        albert_rect.y = 450    # Posição vertical do Albert
        alberts.append(albert)
        alberts_rect.append(albert_rect)
        albert_active = True  # Marcar que Albert está ativo
    return albert_active

# Função para desenhar Albert
def draw_albert(alberts, alberts_rect, display):
    for i in range(len(alberts)):
        display.blit(alberts[i], alberts_rect[i])

# Função para mover Albert
def move_albert(alberts_rect, albert_speed):
    for i in range(len(alberts_rect)):
        alberts_rect[i].x -= albert_speed  # Movendo Albert para a esquerda
        if alberts_rect[i].x < -80:  # Se Albert sair da tela pela esquerda
            alberts_rect.pop(i)  # Remover Albert da lista
            return True  # Indicar que Albert saiu da tela
    return False

# Função para detectar colisão com Albert
def check_collision_with_albert(alberts_rect, personagem_rect, lifes):
    for i in range(len(alberts_rect)):
        if personagem_rect.colliderect(alberts_rect[i]):  # Se o personagem colidir com Albert
            print("Colisão com Albert! Você perdeu uma vida.")
            lifes -= 1  # Jogador perde uma vida
            return lifes, True  # Retorna as vidas e marca colisão
    return lifes, False


# DEFINIÇÃO DOS PERSONAGENS

display = game_start(1080, 720)

bg_image = pygame.image.load("testes/imagem_bg.jpg")
bg_image = pygame.transform.scale(bg_image, (1080, 720))

personagem = pygame.image.load("testes/newton_posição_frente.png")
personagem = pygame.transform.scale(personagem, (140, 240))
personagem_rect = personagem.get_rect()
personagem_rect.x = 0
personagem_rect.y = 450

life_img = pygame.image.load("testes/heart.png")
life_img = pygame.transform.scale(life_img, (40, 40)) 
life_rect = life_img.get_rect()

font = pygame.font.Font(None, 32)
text_color = (0,0,0)

# DEFINIR VÁRIAVEIS
lifes = 6
score = 0
storage = 0
cronometro = 0
pear_speed = 2
apple_speed = 2.5
last_update = pygame.time.get_ticks()
current_frame = 0
estado_de_jogo = "jogando"
restart_apples = 0
personagem_speed = 6
distancia_para_nova_maca = 690
distancia_para_nova_pera = 720
posicoes_usadas = []  
apples = []
apples_rect = []
apples_losts = 0
pears = []
pears_rect = []
cont = 0
apples_golden = []
apples_golden_rect = []
condicao_queda = False

apple_golden_cont = 0



create_apple(apples, apples_rect, cronometro, posicoes_usadas)
create_pear(pears, pears_rect, cronometro, posicoes_usadas)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if estado_de_jogo == "jogando":

        personagem_rect = mover_player(keys, personagem_rect, personagem_speed)

        apple_speed, personagem_speed, distancia_para_nova_maca = temporizador_maca(
            cronometro, apple_speed, personagem_speed, distancia_para_nova_maca)
        
        pear_speed, distancia_para_nova_pera = temporizador_pera(cronometro,pear_speed,distancia_para_nova_pera)

        apples , apples_rect , apples_losts  = cair_apples(apples,apples_rect,apple_speed,apples_losts,distancia_para_nova_maca)

        apples_golden,apples_golden_rect,condicao_queda = cair_apples_golden(apples_golden,apples_golden_rect,apple_speed,condicao_queda,lifes,cronometro,apples_golden)


        pears , pears_rect  = cair_pears(pears,pears_rect,pear_speed,cronometro,distancia_para_nova_pera ) 

        apples_golden,apples_golden_rect,captured_apples_golden , lifes,score,apple_golden_cont = capture_apples_golden(apples_golden,apples_golden_rect,personagem_rect,lifes,score,apple_golden_cont)

        apples, apples_rect, captured_apples, score, restart_apples= capture_apples(apples, apples_rect, personagem_rect, score,restart_apples)

        if captured_apples:
            create_apple(apples, apples_rect, cronometro, posicoes_usadas)

        pears, pears_rect, captured_pears, storage = capture_pears(pears, pears_rect, personagem_rect, storage)

        if captured_apples_golden:
            condicao_queda = False
          
        if captured_pears:
            create_pear(pears, pears_rect, cronometro, posicoes_usadas)

        lifes, estado_de_jogo , storage, apples_losts,restart_apples,cronometro = lifes_controls(lifes,estado_de_jogo,storage,apples_losts,restart_apples,cronometro)
        
       
        display.blit(bg_image, (0, 0))
        draw_apples(apples, apples_rect, display)
        draw_pears(pears, pears_rect, display, cronometro)
        draw_apple_golden(apples_golden, apples_golden_rect, display)

        text = font.render("Score: " + str(score), True, text_color)
        display.blit(text, (10, 50))
        display.blit(personagem, personagem_rect)
        draw_lifes(life_img, lifes, display)
        if (pygame.time.get_ticks() - last_update) >= 1000:
            cronometro += 1
            last_update = pygame.time.get_ticks()
        

        text2 = font.render("Time: " + str(cronometro) + "s", True, text_color)
        display.blit(text2, (10, 80))

    if estado_de_jogo == "fim_de_jogo":
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
        if keys[pygame.K_r]:
            lifes = 6
            score = 0
            restart_apples = 0
            storage = 0
            cronometro = 0
            last_update = pygame.time.get_ticks()
            apple_speed = 2.5
            pear_speed = 2
            current_frame = 0
            personagem_speed = 6
            distancia_para_nova_maca = 690
            distancia_para_nova_pera = 720
            estado_de_jogo = "jogando"
            posicoes_usadas = []  
            apples = []
            apples_rect = []
            apples_losts = 0
            pears = []
            pears_rect = []
            create_apple(apples, apples_rect, cronometro, posicoes_usadas)
            create_pear(pears, pears_rect, cronometro, posicoes_usadas)

         

        display.blit(bg_image, (0, 0))
        text_fim = font.render(
            "Parabens, voce fez " + str(score) + " pontos", True, text_color
        )
        display.blit(text_fim, (350, 200))
        text_restart = font.render("Pressione R para reiniciar", True, text_color)
        display.blit(text_restart, (350, 300))
        text_quit = font.render("Pressione Q para sair", True, text_color)
        display.blit(text_quit, (350, 350))
    print(condicao_queda)
    pygame.display.flip()
    time.sleep(0.015)