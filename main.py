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
ROXO = (128, 0, 128)  # Cor roxa

# Definições de bola
bola_raio = 10
bola_x = largura // 2
bola_y = altura - 100
velocidade_bola_x = 1
velocidade_bola_y = -1

# Pontuação inicial
pontuacao = 0

# Definições de obstáculos
obstaculos = [
    pygame.Rect(100, 200, 50, 20),
    pygame.Rect(300, 350, 80, 20),
    pygame.Rect(500, 100, 60, 20),
    pygame.Rect(650, 250, 70, 20)
]

# Definições dos flippers
flipper_largura = 100
flipper_altura = 20
flipper_y = altura - 50
flipper_esquerdo_x = 50
flipper_direito_x = largura - flipper_largura - 50

# Variáveis para controlar os flippers
flipper_esquerdo_apertado = False
flipper_direito_apertado = False

# Loop principal do jogo
while True:
    # Lidar com eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                flipper_esquerdo_apertado = True
            elif event.key == K_RIGHT:
                flipper_direito_apertado = True
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                flipper_esquerdo_apertado = False
            elif event.key == K_RIGHT:
                flipper_direito_apertado = False

    # Atualizar posição dos flippers
    if flipper_esquerdo_apertado:
        flipper_esquerdo_x += 1
    else:
        flipper_esquerdo_x -= 1

    if flipper_direito_apertado:
        flipper_direito_x -= 1
    else:
        flipper_direito_x += 1

    # Limitar a posição dos flippers dentro dos limites da tela
    flipper_esquerdo_x = max(0, flipper_esquerdo_x)
    flipper_esquerdo_x = min(largura - flipper_largura, flipper_esquerdo_x)

    flipper_direito_x = max(0, flipper_direito_x)
    flipper_direito_x = min(largura - flipper_largura, flipper_direito_x)

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
        # Verificar se a bola atingiu a parte inferior dos flippers
        if bola_y + bola_raio >= flipper_y + flipper_altura:
            print("Fim de jogo!")
            pygame.quit()
            sys.exit()
        bola_y = altura - bola_raio

    # Verificar colisão com os obstáculos
    for obstaculo in obstaculos:
        if obstaculo.colliderect(pygame.Rect(bola_x - bola_raio, bola_y - bola_raio, bola_raio * 2, bola_raio * 2)):
            velocidade_bola_y *= -1
            pontuacao += 1

    # Verificar colisão com os flippers
    flipper_esquerdo = pygame.Rect(flipper_esquerdo_x, flipper_y, flipper_largura, flipper_altura)
    flipper_direito = pygame.Rect(flipper_direito_x, flipper_y, flipper_largura, flipper_altura)
    
    if flipper_esquerdo.colliderect(pygame.Rect(bola_x - bola_raio, bola_y - bola_raio, bola_raio * 2, bola_raio * 2)):
        velocidade_bola_y *= -1
        velocidade_bola_x = abs(velocidade_bola_x)
    elif flipper_direito.colliderect(pygame.Rect(bola_x - bola_raio, bola_y - bola_raio, bola_raio * 2, bola_raio * 2)):
        velocidade_bola_y *= -1
        velocidade_bola_x = -abs(velocidade_bola_x)

    # Desenhar elementos na tela
    tela.fill(BRANCO)
    pygame.draw.circle(tela, AZUL, (bola_x, bola_y), bola_raio)

    for obstaculo in obstaculos:
        pygame.draw.rect(tela, VERMELHO, obstaculo)

    # Desenhar os flippers na tela
    pygame.draw.rect(tela, ROXO, (flipper_esquerdo_x, flipper_y, flipper_largura, flipper_altura))
    pygame.draw.rect(tela, ROXO, (flipper_direito_x, flipper_y, flipper_largura, flipper_altura))

    # Atualizar tela
    pygame.display.update()

