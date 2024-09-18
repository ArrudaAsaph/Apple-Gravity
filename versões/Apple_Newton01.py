import sys

import time

import pygame

pygame.init()

largura = 1080
altura = 720
tamanho = largura , altura
tela = pygame.display.set_mode(tamanho)

bg_image = pygame.image.load(("imgs/imagem_bg.jpg"))
bg_image = pygame.transform.scale(bg_image,(1080,720))
personagem = pygame.image.load("imgs/newton_posição_frente.png")
personagem = pygame.transform.scale(personagem, (140, 240))
personagem_rect = personagem.get_rect()
personagem_rect.x = 0
personagem_rect.y = 450

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
    tela.blit(bg_image, (0, 0))
    tela.blit(personagem,personagem_rect)
    pygame.display.flip()
    time.sleep(0.015)
a