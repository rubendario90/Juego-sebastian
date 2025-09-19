import pygame
import random
from config.settings import *

class Platform:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        
        # Colores para el diseño de arena
        self.color_sand = (237, 201, 175)      # Tono arena claro
        self.color_sand_dark = (194, 150, 130)  # Tono arena más oscuro
        self.color_cracks = (139, 69, 19)       # Marrón para grietas
        self.color_borde = (139, 90, 43)        # Marrón oscuro para bordes
        
        # Generar posiciones aleatorias para las grietas
        self.grietas = self._generar_grietas()

    def _generar_grietas(self):
        grietas = []
        num_grietas = random.randint(3, 6)
        for _ in range(num_grietas):
            start_x = random.randint(self.x + 5, self.x + self.ancho - 20)
            start_y = random.randint(self.y + 5, self.y + self.alto - 5)
            end_x = start_x + random.randint(10, 30)
            end_y = start_y + random.randint(-3, 3)
            end_x = min(end_x, self.x + self.ancho - 5)
            grietas.append([(start_x, start_y), (end_x, end_y)])
            if random.random() < 0.3:
                v_start_x = random.randint(self.x + 5, self.x + self.ancho - 5)
                v_start_y = random.randint(self.y + 5, self.y + self.alto - 15)
                v_end_x = v_start_x + random.randint(-2, 2)
                v_end_y = v_start_y + random.randint(8, 15)
                v_end_y = min(v_end_y, self.y + self.alto - 5)
                grietas.append([(v_start_x, v_start_y), (v_end_x, v_end_y)])
        return grietas

    def dibujar(self, pantalla):
        # Dibujar la base de la plataforma (arena)
        pygame.draw.rect(pantalla, self.color_sand, (self.x, self.y, self.ancho, self.alto))
        
        # Sombra superior izquierda
        pygame.draw.rect(pantalla, (245, 222, 179), (self.x + 2, self.y + 2, self.ancho - 4, 3))
        pygame.draw.rect(pantalla, (245, 222, 179), (self.x + 2, self.y + 2, 3, self.alto - 4))
        
        # Sombra inferior derecha
        pygame.draw.rect(pantalla, self.color_sand_dark, (self.x + 3, self.y + self.alto - 5, self.ancho - 6, 3))
        pygame.draw.rect(pantalla, self.color_sand_dark, (self.x + self.ancho - 5, self.y + 3, 3, self.alto - 6))
        
        # Dibujar grietas
        for grieta in self.grietas:
            pygame.draw.line(pantalla, self.color_cracks, grieta[0], grieta[1], 2)
            pygame.draw.line(pantalla, (120, 60, 20), grieta[0], grieta[1], 1)
        
        # Dibujar borde exterior
        pygame.draw.rect(pantalla, self.color_borde, (self.x, self.y, self.ancho, self.alto), 2)
        
        # Puntos de desgaste
        for _ in range(random.randint(2, 5)):
            punto_x = random.randint(self.x + 3, self.x + self.ancho - 3)
            punto_y = random.randint(self.y + 3, self.y + self.alto - 3)
            pygame.draw.circle(pantalla, self.color_sand_dark, (punto_x, punto_y), 1)

class DesertPlatform(Platform):
    def dibujar(self, pantalla):
        super().dibujar(pantalla)
        
        # Dibujar cactus
        cactus_x = self.x + self.ancho // 2
        cactus_y = self.y + self.alto - 5
        pygame.draw.rect(pantalla, (34, 139, 34), (cactus_x - 5, cactus_y - 15, 10, 15))  # Cuerpo
        pygame.draw.polygon(pantalla, (34, 139, 34), [(cactus_x - 5, cactus_y - 15), (cactus_x, cactus_y - 25), (cactus_x + 5, cactus_y - 15)])  # Parte superior
        
        # Dibujar árbol
        tree_x = self.x + 10
        tree_y = self.y + self.alto - 5
        pygame.draw.rect(pantalla, (139, 69, 19), (tree_x - 2, tree_y - 10, 4, 10))  # Tronco
        pygame.draw.circle(pantalla, (34, 139, 34), (tree_x, tree_y - 15), 8)  # Copa
        
        # Dibujar sol (solo en la plataforma más alta)
        if self.y < 100:  # Ajusta según tu diseño
            sol_x = self.x + self.ancho // 2
            sol_y = self.y - 30
            pygame.draw.circle(pantalla, (255, 215, 0), (sol_x, sol_y), 20)
            pygame.draw.circle(pantalla, (255, 255, 0), (sol_x, sol_y), 18)

# Ejemplo de uso (comentado para evitar conflictos)
# pantalla = pygame.display.set_mode((800, 600))
# plataformas = [
#     DesertPlatform(150, 500, 100, 20),
#     DesertPlatform(200, 400, 100, 20),
#     DesertPlatform(250, 300, 100, 20),
#     DesertPlatform(300, 200, 100, 20)
# ]
# for plataforma in plataformas:
#     plataforma.dibujar(pantalla)
# pygame.display.flip()