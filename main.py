import sys
sys.path.append('Game')
sys.path.append('config')

from Game.Game_manager import GameManager

if __name__ == "__main__":
    juego = GameManager()
    juego.run()