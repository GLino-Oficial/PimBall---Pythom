import pygame
import sys
from pygame.locals import *

# Inicialização do Pygame
pygame.init()

# Definições de tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pinball")

# Cores
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# Definições de raquetes
raquete_largura = 150
raquete_altura = 10
raquete_y = altura - 30
velocidade_raquete = 10

# Raquete esquerda
raquete_esquerda_x = 0

# Raquete direita
raquete_direita_x = largura - raquete_largura

# Definições de bola
bola_raio = 10
bola_x = largura // 2
bola_y = altura - 100
velocidade_bola_x = 5
velocidade_bola_y = -5

# Pontuação inicial
pontuacao = 0

# Definições de obstáculos
obstaculos = [
    pygame.Rect(100, 200, 50, 20),
    pygame.Rect(300, 350, 80, 20),
    pygame.Rect(500, 100, 60, 20),
    pygame.Rect(650, 250, 70, 20)
]

# Loop principal do jogo
while True:
    # Lidar com eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Verificar teclas pressionadas
    keys = pygame.key.get_pressed()
    if keys[K_a] and raquete_y > 0:
        raquete_y -= velocidade_raquete
    if keys[K_d] and raquete_y > 0:
        raquete_y += velocidade_raquete

    if keys[K_LEFT] and raquete_y > 0:
        raquete_y -= velocidade_raquete
    if keys[K_RIGHT] and raquete_y > 0:
        raquete_y += velocidade_raquete

    # Atualizar posição da bola
    bola_x += velocidade_bola_x
    bola_y += velocidade_bola_y

    # Limitar a bola dentro dos limites da tela
    if bola_x - bola_raio <= 0 or bola_x + bola_raio >= largura:
        velocidade_bola_x *= -1
    if bola_y - bola_raio <= 0:
        velocidade_bola_y *= -1
    if bola_y + bola_raio >= altura:
        velocidade_bola_y *= -1
        bola_y = altura - bola_raio

    # Verificar colisão com a raquete esquerda
    if (bola_y + bola_raio >= raquete_y and
        bola_x >= raquete_esquerda_x and
        bola_x <= raquete_esquerda_x + raquete_largura):
        velocidade_bola_y *= -1

    # Verificar colisão com a raquete direita
    if (bola_y + bola_raio >= raquete_y and
        bola_x >= raquete_direita_x and
        bola_x <= raquete_direita_x + raquete_largura):
        velocidade_bola_y *= -1

    # Verificar colisão com os obstáculos
    for obstaculo in obstaculos:
        if obstaculo.colliderect(pygame.Rect(bola_x - bola_raio, bola_y - bola_raio, bola_raio * 2, bola_raio * 2)):
            velocidade_bola_y *= -1
            pontuacao += 1

    # Desenhar elementos na tela
    tela.fill(BRANCO)
    pygame.draw.rect(tela, AZUL, (raquete_esquerda_x, raquete_y, raquete_largura, raquete_altura))
    pygame.draw.rect(tela, AZUL, (raquete_direita_x, raquete_y, raquete_largura, raquete_altura))
    pygame.draw.circle(tela, AZUL, (bola_x, bola_y), bola_raio)

    for obstaculo in obstaculos:
        pygame.draw.rect(tela, VERMELHO, obstaculo)

    # Desenhar pontuação
    fonte = pygame.font.Font(None, 36)
    texto = fonte.render("Pontuação: " + str(pontuacao), True, AZUL)
    tela.blit(texto, (10, 10))

    # Atualizar tela
    pygame.display.update()

