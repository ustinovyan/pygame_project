import os
import sys
import pygame
from pygame import *
import pygame_gui
import random

pygame.mixer.pre_init()
pygame.init()

# Размеры окна
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

CAPTION = "Knight adventure"  # Название игры
ICON_IMAGE = "data/logo_image.png"  # Икока игры

# Звуки
JUMP_SOUND = pygame.mixer.Sound("sounds/jump.wav")
COIN_SOUND = pygame.mixer.Sound("sounds/pickup_coin.wav")
POWERUP_SOUND = pygame.mixer.Sound("sounds/powerup.wav")
HURT_SOUND = pygame.mixer.Sound("sounds/hurt.ogg")
DIE_SOUND = pygame.mixer.Sound("sounds/death.wav")
LEVELUP_SOUND = pygame.mixer.Sound("sounds/level_up.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("sounds/game_over.wav")

FPS = 120  # Частота обновлений

# Размеры персонажа
PLAYER_WIDTH = 25
PLAYER_HEIGHT = 35

MOVE_SPEED = 1
JUMP_POWER = 20
GRAVITY = 0.35

# Размер одного экземпляра платформы
PLATFORM_WIDTH = 320
PLATFORM_HEIGHT = 32

# Используемые цвета
BLUE = (22, 105, 130)
WHITE = (255, 255, 255)
BLACK = (30, 25, 50)

sound_on = True
