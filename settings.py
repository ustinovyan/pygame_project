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
HURT_SOUND = pygame.mixer.Sound("sounds/WOO.mp3")
DIE_SOUND = pygame.mixer.Sound("sounds/death.wav")
LEVELUP_SOUND = pygame.mixer.Sound("sounds/level_up.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("sounds/game_over.wav")

FPS = 120  # Частота обновлений

# Размеры персонажа
PLAYER_SIZE = PLAYER_WIDTH, PLAYER_HEIGHT = 150, 150

MOVE_SPEED = 2
JUMP_POWER = 30
GRAVITY = 0.35

# Размер одного экземпляра платформы
PLATFORM_WIDTH = 320
PLATFORM_HEIGHT = 32

# Используемые цвета
BLUE = (22, 105, 130)
WHITE = (255, 255, 255)
BLACK = (30, 25, 50)

sound_on = True

COIN_SIZE = COIN_WIDTH, COIN_HEIGHT = 50, 50
ENEMY_SIZE = ENEMY_WIDTH, ENEMY_HEIGHT = 100, 100
FLAG_SIZE = FLAG_WIDTH, FLAG_HEIGHT = 100, 100