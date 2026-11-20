# Snake Pygame

Juego Snake desarrollado con Python y Pygame.

## Requisitos

- Python 3.9 o superior
- Pygame

## Instalacion

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
python snake_png.py
```

Si faltan las imagenes, generarlas con:

```bash
python crear_imagenes.py
```

## Controles

- Flechas: mover la serpiente
- `P`: pausar o continuar
- `Esc`: salir
- `C`: jugar otra partida despues de perder
- `Q`: salir desde la pantalla de derrota

El record se guarda localmente en `highscore.txt`.