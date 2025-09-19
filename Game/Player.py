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

        # Movimiento mejorado para plataformas tipo Mario
        self.velocidad = 5
        self.velocidad_maxima = 8
        self.aceleracion = 0.8
        self.friccion = 0.85
        self.velocidad_actual = 0
        
        # Sistema de salto mejorado
        self.velocidad_salto = -15
        self.velocidad_salto_min = -8  # Salto variable
        self.gravedad = 0.8
        self.gravedad_caida = 1.2  # Caída más rápida
        self.saltando = False
        self.en_suelo = False
        
        # Mecánicas tipo Mario
        self.coyote_time = 0.1  # Tiempo para saltar después de salir de plataforma
        self.coyote_timer = 0
        self.jump_buffer_time = 0.1  # Buffer para saltos anticipados
        self.jump_buffer_timer = 0
        self.puede_doble_salto = False
        self.doble_salto_usado = False

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
        
        # Movimiento horizontal mejorado con aceleración
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocidad_actual -= self.aceleracion
            self.velocidad_actual = max(self.velocidad_actual, -self.velocidad_maxima)
            self.facing_right = False
            self.state = "walking"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocidad_actual += self.aceleracion
            self.velocidad_actual = min(self.velocidad_actual, self.velocidad_maxima)
            self.facing_right = True
            self.state = "walking"
        else:
            # Aplicar fricción cuando no se presiona ninguna tecla
            self.velocidad_actual *= self.friccion
            if abs(self.velocidad_actual) < 0.1:
                self.velocidad_actual = 0
            self.state = "idle" if abs(self.velocidad_actual) < 0.5 else "walking"
        
        # Aplicar movimiento horizontal
        self.x += self.velocidad_actual
        
        # Limites de pantalla
        if self.x < 0:
            self.x = 0
            self.velocidad_actual = 0
        elif self.x > ancho_ventana - self.ancho:
            self.x = ancho_ventana - self.ancho
            self.velocidad_actual = 0
        
        # Sistema de salto mejorado
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.jump_buffer_timer = self.jump_buffer_time
        
        # Reducir timers
        if self.coyote_timer > 0:
            self.coyote_timer -= 1/60  # Asumiendo 60 FPS
        if self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= 1/60

    def actualizar(self, plataformas):
        # Guardar posición anterior para detectar aterrizajes
        y_anterior = self.y
        
        # Aplicar gravedad
        if not self.en_suelo:
            if self.velocidad_salto < 0:
                # Gravedad normal durante subida
                self.velocidad_salto += self.gravedad
            else:
                # Gravedad más fuerte durante caída
                self.velocidad_salto += self.gravedad_caida
        
        # Aplicar velocidad vertical
        self.y += self.velocidad_salto
        
        # Detectar si estaba en el suelo previamente
        estaba_en_suelo = self.en_suelo
        self.en_suelo = False
        
        # Detectar colisión con plataformas
        for plataforma in plataformas:
            if (
                self.x + self.ancho > plataforma.x and
                self.x < plataforma.x + plataforma.ancho and
                self.y + self.alto > plataforma.y and
                self.y + self.alto < plataforma.y + plataforma.alto + 10  # Margen de error
            ):
                # Solo aterrizar si venía desde arriba
                if y_anterior + self.alto <= plataforma.y + 5:
                    self.y = plataforma.y - self.alto
                    self.en_suelo = True
                    self.velocidad_salto = 0
                    self.doble_salto_usado = False
                    
                    # Si acabamos de aterrizar, reiniciar coyote time
                    if not estaba_en_suelo:
                        self.coyote_timer = self.coyote_time
        
        # Coyote time: permitir salto poco después de salir de plataforma
        if estaba_en_suelo and not self.en_suelo:
            self.coyote_timer = self.coyote_time
        
        # Procesar salto con buffer y coyote time
        if self.jump_buffer_timer > 0:
            if (self.en_suelo or self.coyote_timer > 0) and not self.saltando:
                # Salto normal
                self.velocidad_salto = -15
                self.saltando = True
                self.en_suelo = False
                self.coyote_timer = 0
                self.jump_buffer_timer = 0
            elif self.puede_doble_salto and not self.doble_salto_usado and self.saltando:
                # Doble salto
                self.velocidad_salto = -13
                self.doble_salto_usado = True
                self.jump_buffer_timer = 0
        
        # Finalizar salto si se suelta la tecla (salto variable)
        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
            if self.velocidad_salto < self.velocidad_salto_min:
                self.velocidad_salto = self.velocidad_salto_min
        
        # Límite inferior de pantalla
        if self.y > alto_ventana:
            self.y = alto_ventana - self.alto
            self.en_suelo = True
            self.velocidad_salto = 0
        
        # Actualizar estado de salto
        if self.en_suelo:
            self.saltando = False
        
        # Actualizar animación
        self.frame += self.animation_speed
        if self.state == "walking":
            if self.frame >= len(self.sprites_walk):
                self.frame = 0
        else:
            self.frame = 0

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