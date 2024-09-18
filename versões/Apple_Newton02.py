import sys
import random
import time
import pygame

def game_start(w, h):
    pygame.init()
    tamanho = w, h
    tela = pygame.display.set_mode(tamanho)
    pygame.display.set_caption("Apple Newton")
    return tela

def create_apple(apples, apples_rect):
    ranges = [(665, 50), (800, 123), (480, 123), (550, 115), (230, 115), 
              (265, 200), (430, 200), (835, 200), (900, 180), (160, 180), 
              (260, 280), (910, 280), (910, 330), (320, 330)]
    apple = pygame.image.load(("imgs/maca.png"))
    apple = pygame.transform.scale(apple, (60, 70))
    apple_rect = apple.get_rect()
    n_aleatorio = random.randrange(14)
    teste = ranges[n_aleatorio]
    apple_rect.x, apple_rect.y = teste
    apples.append(apple)
    apples_rect.append(apple_rect)

def draw_apples(apples, apples_rect, display):
    for i in range(len(apples)):
        display.blit(apples[i], apples_rect[i])

display = game_start(1080, 720)

apples = []
apples_rect = []
for i in range(0, 10):
    create_apple(apples, apples_rect)

bg_image = pygame.image.load(("imgs/imagem_bg.jpg"))
bg_image = pygame.transform.scale(bg_image, (1080, 720))
personagem = pygame.image.load("imgs/newton_posição_frente.png")
personagem = pygame.transform.scale(personagem, (140, 240))
personagem_rect = personagem.get_rect()
personagem_rect.x = 0
personagem_rect.y = 450


current_apple = 0


apple_speed = 2

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        personagem_rect.x -= 7.5
        if personagem_rect.left < -30:
            personagem_rect.left = -30
    if keys[pygame.K_RIGHT]:
        personagem_rect.x += 7.5
        if personagem_rect.right > 1200:
            personagem_rect.right = 1200

    if current_apple < len(apples_rect):
        apples_rect[current_apple].y += apple_speed

        if apples_rect[current_apple].y > 720:
            current_apple += 1


    display.blit(bg_image, (0, 0))
    draw_apples(apples, apples_rect, display)
    display.blit(personagem, personagem_rect)
    
    pygame.display.flip()
    time.sleep(0.015)
