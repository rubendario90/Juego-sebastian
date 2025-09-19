#!/usr/bin/env python3
import os
import sys
import pygame

# Disable audio to avoid ALSA errors
os.environ['SDL_AUDIODRIVER'] = 'dummy'

# Set up the paths
sys.path.append('Game')
sys.path.append('config')

def capture_game_screenshot():
    """Capture a screenshot of the improved game"""
    try:
        from Game.Game_manager import GameManager
        
        # Initialize pygame with no audio
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=1024)
        pygame.mixer.init()
        
        print("Inicializando juego para captura...")
        juego = GameManager()
        
        # Simulate some gameplay to show features
        # Move player to a better position for screenshot
        juego.zombi.x = 300
        juego.zombi.y = 400
        
        # Update the game once to render everything
        juego.actualizar_juego(1/60)
        juego.dibujar_todo()
        
        # Save screenshot
        pygame.image.save(juego.pantalla, "/tmp/zombie_mario_screenshot.png")
        print("Captura guardada en /tmp/zombie_mario_screenshot.png")
        
        # Print game state for verification
        print(f"Estado del juego: {juego.game_state}")
        print(f"Posición del zombi: ({juego.zombi.x}, {juego.zombi.y})")
        print(f"Plataformas en el nivel: {len(juego.plataformas)}")
        print(f"Monedas en el nivel: {len(juego.coins)}")
        print(f"Cerebros en el nivel: {len(juego.brains)}")
        print(f"Enemigos en el nivel: {len(juego.enemies)}")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"Error durante la captura: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = capture_game_screenshot()
    sys.exit(0 if success else 1)