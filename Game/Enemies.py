import pygame
import random
import math
from config.settings import *

class BasicEnemy:
    def __init__(self, x, y, platform_x, platform_width):
        self.x = x
        self.y = y
        self.ancho = 40
        self.alto = 30
        self.velocidad = 1.5
        self.direccion = 1  # 1 = derecha, -1 = izquierda
        self.platform_x = platform_x
        self.platform_width = platform_width
        self.alive = True
        self.animation_timer = 0
        
        # Límites de la plataforma
        self.limite_izq = platform_x
        self.limite_der = platform_x + platform_width - self.ancho
        
    def actualizar(self):
        if self.alive:
            self.animation_timer += 0.1
            
            # Mover enemigo
            self.x += self.velocidad * self.direccion
            
            # Cambiar dirección en los bordes de la plataforma
            if self.x <= self.limite_izq or self.x >= self.limite_der:
                self.direccion *= -1
                self.x = max(self.limite_izq, min(self.limite_der, self.x))
    
    def dibujar(self, pantalla):
        if self.alive:
            # Dibujar enemigo zombie simple
            # Cuerpo verde oscuro
            body_color = (100, 150, 100)
            pygame.draw.ellipse(pantalla, body_color, 
                              (self.x, self.y, self.ancho, self.alto))
            
            # Ojos rojos
            eye_size = 4
            if self.direccion == 1:  # Mirando derecha
                pygame.draw.circle(pantalla, (255, 0, 0), 
                                 (int(self.x + self.ancho * 0.7), int(self.y + 8)), eye_size)
            else:  # Mirando izquierda
                pygame.draw.circle(pantalla, (255, 0, 0), 
                                 (int(self.x + self.ancho * 0.3), int(self.y + 8)), eye_size)
            
            # Efectos de movimiento
            wave_offset = math.sin(self.animation_timer) * 2
            pygame.draw.ellipse(pantalla, (80, 120, 80), 
                              (self.x, self.y + wave_offset, self.ancho, self.alto//2))
    
    def verificar_colision_player(self, player):
        if self.alive:
            if (player.x < self.x + self.ancho and
                player.x + player.ancho > self.x and
                player.y < self.y + self.alto and
                player.y + player.alto > self.y):
                
                # Verificar si el jugador está saltando sobre el enemigo
                if player.velocidad_salto > 0 and player.y < self.y - 10:
                    # Jugador mata al enemigo saltando sobre él
                    self.alive = False
                    player.velocidad_salto = -8  # Pequeño rebote
                    return "enemy_killed"
                else:
                    # Enemigo daña al jugador
                    return "player_hit"
        return None

class FlyingEnemy:
    def __init__(self, x, y, patrol_range=100):
        self.start_x = x
        self.x = x
        self.y = y
        self.ancho = 35
        self.alto = 25
        self.velocidad = 2
        self.patrol_range = patrol_range
        self.alive = True
        self.animation_timer = 0
        self.direction_timer = 0
        self.move_pattern = 0  # 0 = horizontal, 1 = vertical, 2 = circular
        
    def actualizar(self):
        if self.alive:
            self.animation_timer += 0.2
            self.direction_timer += 0.05
            
            # Patrón de movimiento horizontal ondulante
            self.x += math.sin(self.direction_timer) * self.velocidad
            self.y += math.cos(self.direction_timer * 2) * 0.5
            
            # Limitar al rango de patrullaje
            if abs(self.x - self.start_x) > self.patrol_range:
                self.x = self.start_x + (self.patrol_range if self.x > self.start_x else -self.patrol_range)
    
    def dibujar(self, pantalla):
        if self.alive:
            # Dibujar murciélago zombie
            wing_flap = math.sin(self.animation_timer) * 3
            
            # Cuerpo
            pygame.draw.ellipse(pantalla, (60, 60, 80), 
                              (self.x + 10, self.y + 8, self.ancho - 20, self.alto - 10))
            
            # Alas
            wing_points_left = [
                (self.x, self.y + 10 + wing_flap),
                (self.x + 15, self.y + 5),
                (self.x + 10, self.y + 15)
            ]
            wing_points_right = [
                (self.x + self.ancho, self.y + 10 + wing_flap),
                (self.x + self.ancho - 15, self.y + 5),
                (self.x + self.ancho - 10, self.y + 15)
            ]
            
            pygame.draw.polygon(pantalla, (40, 40, 60), wing_points_left)
            pygame.draw.polygon(pantalla, (40, 40, 60), wing_points_right)
            
            # Ojos rojos brillantes
            pygame.draw.circle(pantalla, (255, 50, 50), 
                             (int(self.x + 12), int(self.y + 10)), 2)
            pygame.draw.circle(pantalla, (255, 50, 50), 
                             (int(self.x + 18), int(self.y + 10)), 2)
    
    def verificar_colision_player(self, player):
        if self.alive:
            if (player.x < self.x + self.ancho and
                player.x + player.ancho > self.x and
                player.y < self.y + self.alto and
                player.y + player.alto > self.y):
                return "player_hit"
        return None