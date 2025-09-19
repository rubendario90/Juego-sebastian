import pygame
import sys

pygame.init()

# Constants
ancho_ventana = 800
alto_ventana = 600
FPS = 60

# Colors
color_fondo = (135, 206, 235)  # Cielo azul en lugar de blanco

# Game Colors
COLOR_UI_TEXT = (255, 255, 255)
COLOR_SCORE = (255, 255, 0)
COLOR_GAME_OVER = (255, 0, 0)
COLOR_VICTORY = (0, 255, 0)

# Player colors
COLOR_PIEL_ZOMBI = (144, 238, 144)   # Pale green for zombie skin
COLOR_CAMISA = (180, 100, 0)         # Darker, dirtier orange for tattered shirt
COLOR_PANTALON = (150, 20, 40)       # Faded crimson for torn pants
COLOR_ZAPATOS = (25, 25, 112)        # Midnight blue for worn shoes
COLOR_OJOS = (255, 50, 50)           # Softer red for glowing eyes
COLOR_DIENTES = (200, 200, 200)      # Off-white for decayed teeth