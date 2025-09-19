import pygame
import sys
from config.settings import *
from Player import Player
from Platforms import Platform

class GameManager:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
        pygame.display.set_caption("Juego del Zombi")
        
        # Crear el reloj
        self.reloj = pygame.time.Clock()
        
        # Crear el zombi
        self.zombi = Player(100, 400) 
        print(f"Zombi creado en posición: {self.zombi.x}, {self.zombi.y}")

        # Crear plataformas
        self.plataformas = [
            Platform(100, 500, 200, 20),  # Plataforma 1
            Platform(400, 400, 200, 20),  # Plataforma 2
            Platform(700, 300, 200, 20)   # Plataforma 3
        ]

    def run(self):
        ejecutando = True
        while ejecutando:
            # Manejar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
            
            # Limpiar pantalla (fondo blanco)
            self.pantalla.fill(color_fondo)
            
            # Actualizar y mover el zombi
            self.zombi.mover()
            self.zombi.actualizar(self.plataformas)
            
            # Dibujar plataformas
            for plataforma in self.plataformas:
                plataforma.dibujar(self.pantalla)
            
            # Dibujar el zombi
            self.zombi.dibujar(self.pantalla)
            
            # Actualizar pantalla
            pygame.display.flip()
            self.reloj.tick(FPS)
        
        pygame.quit()
        sys.exit()