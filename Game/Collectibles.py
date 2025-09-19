import pygame
import math
from config.settings import *

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 20
        self.alto = 20
        self.collected = False
        self.animation_timer = 0
        self.bounce_offset = 0
        
    def actualizar(self):
        if not self.collected:
            self.animation_timer += 0.1
            self.bounce_offset = math.sin(self.animation_timer) * 3
    
    def dibujar(self, pantalla):
        if not self.collected:
            # Dibujar moneda dorada con efecto de rebote
            coin_y = self.y + self.bounce_offset
            
            # Círculo exterior dorado
            pygame.draw.circle(pantalla, (255, 215, 0), 
                             (int(self.x + self.ancho/2), int(coin_y + self.alto/2)), 12)
            # Círculo interior más claro
            pygame.draw.circle(pantalla, (255, 255, 150), 
                             (int(self.x + self.ancho/2), int(coin_y + self.alto/2)), 8)
            # Brillos
            pygame.draw.circle(pantalla, (255, 255, 255), 
                             (int(self.x + self.ancho/2 - 3), int(coin_y + self.alto/2 - 3)), 3)
    
    def verificar_colision(self, player):
        if not self.collected:
            if (player.x < self.x + self.ancho and
                player.x + player.ancho > self.x and
                player.y < self.y + self.alto and
                player.y + player.alto > self.y):
                self.collected = True
                return True
        return False

class Brain:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 25
        self.alto = 20
        self.collected = False
        self.animation_timer = 0
        self.pulse_scale = 1.0
        
    def actualizar(self):
        if not self.collected:
            self.animation_timer += 0.15
            self.pulse_scale = 1.0 + math.sin(self.animation_timer) * 0.2
    
    def dibujar(self, pantalla):
        if not self.collected:
            # Dibujar cerebro rosado que pulsa
            brain_size = int(12 * self.pulse_scale)
            center_x = int(self.x + self.ancho/2)
            center_y = int(self.y + self.alto/2)
            
            # Cerebro principal
            pygame.draw.ellipse(pantalla, (255, 192, 203), 
                              (center_x - brain_size, center_y - brain_size//2, 
                               brain_size * 2, brain_size))
            
            # Líneas del cerebro
            pygame.draw.line(pantalla, (200, 150, 150), 
                           (center_x - brain_size//2, center_y - brain_size//4),
                           (center_x + brain_size//2, center_y - brain_size//4), 2)
            pygame.draw.line(pantalla, (200, 150, 150), 
                           (center_x - brain_size//2, center_y + brain_size//4),
                           (center_x + brain_size//2, center_y + brain_size//4), 2)
    
    def verificar_colision(self, player):
        if not self.collected:
            if (player.x < self.x + self.ancho and
                player.x + player.ancho > self.x and
                player.y < self.y + self.alto and
                player.y + player.alto > self.y):
                self.collected = True
                return True
        return False