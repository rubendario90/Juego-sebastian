# Zombie Mario - Plataformero

Un juego de plataformas estilo Mario con temática zombie, construido con Python y Pygame.

## Características del Juego

### Mecánicas Tipo Mario
- **Movimiento mejorado**: Aceleración y fricción realistas
- **Sistema de salto avanzado**: 
  - Salto variable (mantén presionado para saltar más alto)
  - Doble salto habilitado
  - Coyote time (puedes saltar brevemente después de salir de una plataforma)
  - Jump buffering (presiona salto antes de aterrizar)
- **Física mejorada**: Gravedad diferente para subida y caída

### Elementos del Juego
- **Coleccionables**:
  - 🪙 Monedas (100 puntos cada una)
  - 🧠 Cerebros (500 puntos + vida extra)
- **Enemigos**:
  - Zombies básicos que patrullan plataformas
  - Murciélagos voladores con patrones de movimiento
  - Puedes saltar sobre los enemigos para eliminarlos
- **Sistema de vidas**: 3 vidas iniciales, pierdes vida al tocar enemigos o caer
- **Invencibilidad temporal**: Después de recibir daño

### Controles
- **Movimiento**: Flechas ← → o A/D
- **Salto**: Espacio, Flecha ↑ o W
  - Mantén presionado para salto más alto
  - Doble salto disponible en el aire
- **Pausa**: P
- **Reiniciar** (Game Over/Victoria): R

### Objetivo
Recolecta todos los cerebros (🧠) para ganar el nivel mientras evitas a los enemigos y recoges monedas para aumentar tu puntuación.

## Instalación y Ejecución

```bash
# Instalar dependencias
pip install pygame

# Ejecutar el juego
python main.py

# Ejecutar prueba sin audio (para entornos sin sonido)
python test_game.py
```

## Estructura del Código

- `main.py`: Punto de entrada del juego
- `Game/Game_manager.py`: Lógica principal del juego
- `Game/Player.py`: Clase del jugador zombie con mecánicas avanzadas
- `Game/Platforms.py`: Sistema de plataformas con diseño visual
- `Game/Collectibles.py`: Monedas y cerebros coleccionables
- `Game/Enemies.py`: Enemigos básicos y voladores
- `config/settings.py`: Configuración y constantes del juego

## Mejoras Implementadas

1. **Física de movimiento tipo Mario**: Aceleración, fricción, gravedad variable
2. **Sistema de salto avanzado**: Coyote time, jump buffering, doble salto
3. **Nivel estructurado**: Plataformas estratégicamente ubicadas
4. **Sistema de puntuación**: Diferentes valores para coleccionables
5. **Mecánica de enemigos**: Patrullaje y eliminación por salto
6. **Estados de juego**: Victoria, derrota, pausa
7. **UI informativa**: Puntuación, vidas, progreso
8. **Efectos visuales**: Parpadeo de invencibilidad, animaciones