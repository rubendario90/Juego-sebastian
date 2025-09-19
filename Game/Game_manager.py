import pygame
import sys
from config.settings import *
from Player import Player
from Platforms import Platform
from Collectibles import Coin, Brain
from Enemies import BasicEnemy, FlyingEnemy

class GameManager:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
        pygame.display.set_caption("Zombie Mario - Plataformero")
        
        # Crear el reloj
        self.reloj = pygame.time.Clock()
        
        # Estados del juego
        self.game_state = "playing"  # "playing", "paused", "game_over", "victory"
        
        # Sistema de puntuación
        self.score = 0
        self.lives = 3
        self.font = pygame.font.Font(None, 36)
        
        # Crear el zombi jugador
        self.zombi = Player(100, 450) 
        self.zombi.puede_doble_salto = True  # Habilitar doble salto
        print(f"Zombi creado en posición: {self.zombi.x}, {self.zombi.y}")

        # Crear nivel con plataformas más complejas tipo Mario
        self.crear_nivel_1()
        
        # Variables de invencibilidad después de recibir daño
        self.invulnerable_timer = 0
        self.invulnerable_duration = 2.0  # 2 segundos de invencibilidad

    def crear_nivel_1(self):
        """Crear un nivel tipo Mario con plataformas, enemigos y coleccionables"""
        # Plataformas principales del nivel
        self.plataformas = [
            Platform(0, 570, 200, 30),      # Plataforma inicial (suelo)
            Platform(250, 500, 150, 20),    # Primera plataforma elevada
            Platform(450, 420, 120, 20),    # Segunda plataforma
            Platform(600, 350, 100, 20),    # Tercera plataforma más alta
            Platform(150, 380, 80, 20),     # Plataforma intermedia
            Platform(350, 280, 100, 20),    # Plataforma alta
            Platform(550, 200, 150, 20),    # Plataforma superior
            Platform(700, 500, 100, 30),    # Plataforma final
        ]
        
        # Coleccionables estratégicamente ubicados
        self.coins = [
            Coin(180, 460),   # Sobre primera plataforma
            Coin(480, 380),   # Sobre segunda plataforma
            Coin(630, 310),   # Sobre tercera plataforma
            Coin(180, 340),   # Sobre plataforma intermedia
            Coin(380, 240),   # Sobre plataforma alta
            Coin(580, 160),   # Sobre plataforma superior
            Coin(730, 460),   # En plataforma final
        ]
        
        self.brains = [
            Brain(300, 460),  # Premio especial 1
            Brain(400, 240),  # Premio especial en zona alta
            Brain(620, 160),  # Premio especial en la cima
        ]
        
        # Enemigos patrullando plataformas
        self.enemies = [
            BasicEnemy(270, 470, 250, 150),    # En primera plataforma
            BasicEnemy(470, 390, 450, 120),    # En segunda plataforma
            BasicEnemy(720, 470, 700, 100),    # En plataforma final
            FlyingEnemy(400, 300, 80),         # Enemigo volador
            FlyingEnemy(200, 250, 60),         # Otro enemigo volador
        ]

    def run(self):
        ejecutando = True
        while ejecutando:
            delta_time = self.reloj.tick(FPS) / 1000.0  # Delta time en segundos
            
            # Manejar eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r and self.game_state == "game_over":
                        self.reiniciar_juego()
                    elif evento.key == pygame.K_p:
                        self.pausar_juego()
            
            if self.game_state == "playing":
                self.actualizar_juego(delta_time)
            
            self.dibujar_todo()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def actualizar_juego(self, delta_time):
        # Actualizar timer de invencibilidad
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= delta_time
        
        # Actualizar y mover el zombi
        self.zombi.mover()
        self.zombi.actualizar(self.plataformas)
        
        # Actualizar coleccionables
        for coin in self.coins:
            coin.actualizar()
            if coin.verificar_colision(self.zombi):
                self.score += 100
        
        for brain in self.brains:
            brain.actualizar()
            if brain.verificar_colision(self.zombi):
                self.score += 500
                self.lives += 1  # Los cerebros dan vida extra
        
        # Actualizar enemigos
        for enemy in self.enemies:
            enemy.actualizar()
            
            # Solo verificar colisiones si no es invulnerable
            if self.invulnerable_timer <= 0:
                resultado = enemy.verificar_colision_player(self.zombi)
                if resultado == "player_hit":
                    self.lives -= 1
                    self.invulnerable_timer = self.invulnerable_duration
                    # Empujar al jugador hacia atrás
                    self.zombi.velocidad_actual = -5 if self.zombi.facing_right else 5
                    if self.lives <= 0:
                        self.game_state = "game_over"
                elif resultado == "enemy_killed":
                    self.score += 200
        
        # Verificar si el jugador cae fuera de la pantalla
        if self.zombi.y > alto_ventana + 100:
            self.lives -= 1
            self.zombi.x = 100
            self.zombi.y = 450
            self.zombi.velocidad_salto = 0
            self.zombi.velocidad_actual = 0
            if self.lives <= 0:
                self.game_state = "game_over"
        
        # Verificar condición de victoria (recoger todos los cerebros)
        if all(brain.collected for brain in self.brains):
            self.game_state = "victory"
    
    def dibujar_todo(self):
        # Limpiar pantalla con un fondo más atractivo
        self.pantalla.fill((135, 206, 235))  # Color cielo azul
        
        # Dibujar plataformas
        for plataforma in self.plataformas:
            plataforma.dibujar(self.pantalla)
        
        # Dibujar coleccionables
        for coin in self.coins:
            coin.dibujar(self.pantalla)
        
        for brain in self.brains:
            brain.dibujar(self.pantalla)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.dibujar(self.pantalla)
        
        # Dibujar el zombi (con efecto de parpadeo si es invulnerable)
        if self.invulnerable_timer <= 0 or int(self.invulnerable_timer * 10) % 2:
            self.zombi.dibujar(self.pantalla)
        
        # Dibujar UI
        self.dibujar_ui()
        
        # Dibujar mensajes de estado del juego
        if self.game_state == "game_over":
            self.dibujar_game_over()
        elif self.game_state == "victory":
            self.dibujar_victoria()
        elif self.game_state == "paused":
            self.dibujar_pausa()
    
    def dibujar_ui(self):
        # Dibujar puntuación
        score_text = self.font.render(f"Puntos: {self.score}", True, (255, 255, 255))
        self.pantalla.blit(score_text, (10, 10))
        
        # Dibujar vidas
        lives_text = self.font.render(f"Vidas: {self.lives}", True, (255, 255, 255))
        self.pantalla.blit(lives_text, (10, 50))
        
        # Mostrar progreso de cerebros
        brains_collected = sum(1 for brain in self.brains if brain.collected)
        brain_text = self.font.render(f"Cerebros: {brains_collected}/{len(self.brains)}", True, (255, 255, 255))
        self.pantalla.blit(brain_text, (10, 90))
    
    def dibujar_game_over(self):
        # Dibujar pantalla de game over
        overlay = pygame.Surface((ancho_ventana, alto_ventana))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        score_text = self.font.render(f"Puntuación Final: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Presiona R para reiniciar", True, (255, 255, 255))
        
        self.pantalla.blit(game_over_text, (ancho_ventana//2 - 100, alto_ventana//2 - 50))
        self.pantalla.blit(score_text, (ancho_ventana//2 - 120, alto_ventana//2))
        self.pantalla.blit(restart_text, (ancho_ventana//2 - 150, alto_ventana//2 + 50))
    
    def dibujar_victoria(self):
        # Dibujar pantalla de victoria
        overlay = pygame.Surface((ancho_ventana, alto_ventana))
        overlay.set_alpha(180)
        overlay.fill((0, 100, 0))
        self.pantalla.blit(overlay, (0, 0))
        
        victory_text = self.font.render("¡VICTORIA!", True, (255, 255, 0))
        score_text = self.font.render(f"Puntuación Final: {self.score}", True, (255, 255, 255))
        restart_text = self.font.render("Presiona R para jugar de nuevo", True, (255, 255, 255))
        
        self.pantalla.blit(victory_text, (ancho_ventana//2 - 80, alto_ventana//2 - 50))
        self.pantalla.blit(score_text, (ancho_ventana//2 - 120, alto_ventana//2))
        self.pantalla.blit(restart_text, (ancho_ventana//2 - 180, alto_ventana//2 + 50))
    
    def dibujar_pausa(self):
        # Dibujar pantalla de pausa
        overlay = pygame.Surface((ancho_ventana, alto_ventana))
        overlay.set_alpha(120)
        overlay.fill((0, 0, 100))
        self.pantalla.blit(overlay, (0, 0))
        
        pause_text = self.font.render("PAUSADO", True, (255, 255, 255))
        continue_text = self.font.render("Presiona P para continuar", True, (255, 255, 255))
        
        self.pantalla.blit(pause_text, (ancho_ventana//2 - 70, alto_ventana//2 - 25))
        self.pantalla.blit(continue_text, (ancho_ventana//2 - 160, alto_ventana//2 + 25))
    
    def reiniciar_juego(self):
        # Reiniciar el estado del juego
        self.score = 0
        self.lives = 3
        self.game_state = "playing"
        self.invulnerable_timer = 0
        
        # Reiniciar jugador
        self.zombi.x = 100
        self.zombi.y = 450
        self.zombi.velocidad_salto = 0
        self.zombi.velocidad_actual = 0
        self.zombi.en_suelo = False
        
        # Recrear nivel
        self.crear_nivel_1()
    
    def pausar_juego(self):
        if self.game_state == "playing":
            self.game_state = "paused"
        elif self.game_state == "paused":
            self.game_state = "playing"