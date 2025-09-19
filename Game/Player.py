import pygame
from config.settings import *

class Player:
    def __init__(self, x, y):
        # Posición inicial
        self.x = x
        self.y = y

        # Tamaño
        self.ancho = 50
        self.alto = 70

        # Movimiento
        self.velocidad = 7
        self.velocidad_salto = -18
        self.gravedad = 1
        self.salto = False
        self.saltando = False

        # Dirección inicial (mirando a la derecha)
        self.facing_right = True

        # Estado inicial (idle, walking, jumping)
        self.state = "idle"

        # Animación
        self.frame = 0
        self.animation_speed = 0.2

        # Cargar sprites
        self.sprites_idle = [pygame.image.load("assets/images/Imagen 1.png")]  # Cambiar esta línea
        self.sprites_walk = [
            pygame.image.load("assets/images/Imagen 1.png"),
            pygame.image.load("assets/images/Imagen 2.png"),
            pygame.image.load("assets/images/Imagen 3.png")
        ]

        # Escalar los sprites al tamaño del zombi
        self.sprites_idle = [pygame.transform.scale(img, (self.ancho, self.alto)) for img in self.sprites_idle]
        self.sprites_walk = [pygame.transform.scale(img, (self.ancho, self.alto)) for img in self.sprites_walk]

    def mover(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.velocidad
            self.facing_right = False
            self.state = "walking"
        elif keys[pygame.K_RIGHT]:
            self.x += self.velocidad
            self.facing_right = True
            self.state = "walking"
        else:
            self.state = "idle"

        if keys[pygame.K_SPACE] and not self.saltando:
            self.saltando = True
            self.velocidad_salto = -18

    def actualizar(self, plataformas):
        if self.saltando:
            self.y += self.velocidad_salto
            self.velocidad_salto += self.gravedad

            # Detectar colisión con plataformas
            for plataforma in plataformas:
                if (
                    self.x + self.ancho > plataforma.x and
                    self.x < plataforma.x + plataforma.ancho and
                    self.y + self.alto > plataforma.y and
                    self.y + self.alto < plataforma.y + plataforma.alto
                ):
                    self.y = plataforma.y - self.alto
                    self.saltando = False
                    self.velocidad_salto = 0

        # Actualizar el frame de animación
        self.frame += self.animation_speed
        if self.state == "walking":
            if self.frame >= len(self.sprites_walk):
                self.frame = 0
        else:
            self.frame = 0  # Resetear frame si no está caminando

    def dibujar(self, pantalla):
        # Seleccionar el sprite según el estado
        if self.state == "walking":
            sprite = self.sprites_walk[int(self.frame)]
        else:
            sprite = self.sprites_idle[0]

        # Dibujar el sprite
        if self.facing_right:
            pantalla.blit(sprite, (self.x, self.y))
        else:
            flipped_sprite = pygame.transform.flip(sprite, True, False)
            pantalla.blit(flipped_sprite, (self.x, self.y))