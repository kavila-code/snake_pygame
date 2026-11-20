import pygame
import random
import queue
from pathlib import Path

pygame.init()

# Colores (RGB)
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
yellow = (255, 255, 0)
pink = (255, 0, 255)

# Resolución y ventana
diswidth = 600
disheight = 400
dis = pygame.display.set_mode((diswidth, disheight))
pygame.display.set_caption('Snake')

# Variables de la serpiente
snakeblock = 10
snakespeed = 15
maxspeed = 40
points_per_level = 5
compass = {
    'left': [-snakeblock, 0, 'left'],
    'right': [snakeblock, 0, 'right'],
    'up': [0, -snakeblock, 'up'],
    'down': [0, snakeblock, 'down'],
}
opposite = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}

clock = pygame.time.Clock()
Q = queue.Queue(maxsize=10)

# Fuentes
title_font = pygame.font.SysFont('bahnschrift', 60)
font_style = pygame.font.SysFont('bahnschrift', 25)
hud_font = pygame.font.SysFont('bahnschrift', 24)

# Imagen de fondo (PNG), ajustada al tamaño de la ventana
bgd_image = pygame.image.load(Path(__file__).parent / 'background.png').convert()
bgd_image = pygame.transform.scale(bgd_image, (diswidth, disheight))

# Imagen de los segmentos de la serpiente (PNG)
snake_image = pygame.image.load(Path(__file__).parent / '01_image.png').convert()
snake_image = pygame.transform.scale(snake_image, (snakeblock, snakeblock))
snake_image.set_colorkey(pink)

BASE = Path(__file__).parent

highscore_file = BASE / 'highscore.txt'

def load_highscore():
    try:
        return int(highscore_file.read_text().strip())
    except (OSError, ValueError):
        return 0

def save_highscore(value):
    try:
        highscore_file.write_text(str(value))
    except OSError:
        pass

def draw_text(text, font, color, x, y, center=False):
    shadow = font.render(text, True, black)
    label = font.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    dis.blit(shadow, rect.move(2, 2))
    dis.blit(label, rect)

def draw_hud(score, level, highscore):
    draw_text(f'Score: {score}   Nivel: {level}', hud_font, yellow, 8, 6)
    label = f'Record: {highscore}'
    width = hud_font.size(label)[0]
    draw_text(label, hud_font, yellow, diswidth - width - 8, 6)


def oursnake(snakelist):
    for segment in snakelist:
        dis.blit(snake_image, (segment[0], segment[1]))


def new_food(snakelist):
    while True:
        foodx = random.randrange(0, diswidth - snakeblock + 1, snakeblock)
        foody = random.randrange(0, disheight - snakeblock + 1, snakeblock)
        if [foodx, foody] not in snakelist:
            return foodx, foody

def start_screen(highscore):
    while True:
        dis.blit(bgd_image, (0, 0))
        draw_text('SNAKE', title_font, yellow, diswidth // 2, 100, center=True)
        draw_text('Flechas: mover    P: pausa    Esc: salir', font_style, white,
                  diswidth // 2, 190, center=True)
        draw_text(f'Record: {highscore}', font_style, white, diswidth // 2, 230, center=True)
        draw_text('Presiona cualquier tecla para jugar', font_style, green,
                  diswidth // 2, 300, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                return True
        clock.tick(30)

def game_over_screen(score, highscore, new_record):
    while True:
        dis.blit(bgd_image, (0, 0))
        draw_text('You lost!', title_font, red, diswidth // 2, 100, center=True)
        draw_text(f'Score: {score}    Record: {highscore}', font_style, yellow,
                  diswidth // 2, 180, center=True)
        if new_record:
            draw_text('Nuevo record!', font_style, green, diswidth // 2, 215, center=True)
        draw_text('Presiona Q para salir o C para jugar otra vez', font_style, red,
                  diswidth // 2, 300, center=True)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return 'quit'
                if event.key == pygame.K_c:
                    return 'restart'
        clock.tick(30)

def run_game(highscore):
    direction = ''
    x1 = diswidth // 2
    y1 = disheight // 2
    x1_change = 0
    y1_change = 0

    snakelist = []
    snakelength = 1
    foodx, foody = new_food(snakelist)
    paused = False

    while True:
        score = snakelength - 1
        level = score // points_per_level + 1
        speed = min(snakespeed + (level - 1) * 2, maxspeed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit', score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit', score
                if event.key == pygame.K_p:
                    paused = not paused
                elif not paused:
                    keys = {pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right',
                            pygame.K_UP: 'up', pygame.K_DOWN: 'down'}
                    if event.key in keys and direction != opposite[keys[event.key]]:
                        try:
                            Q.put_nowait(keys[event.key])
                        except queue.Full:
                            pass

        if paused:
            draw_text('PAUSA', title_font, yellow, diswidth // 2, disheight // 2, center=True)
            pygame.display.update()
            clock.tick(15)
            continue

        if not Q.empty():
            next_command = Q.get()
            if next_command != opposite.get(direction):
                x1_change, y1_change, direction = compass[next_command]

        x1 += x1_change
        y1 += y1_change

        if x1 >= diswidth or x1 < 0 or y1 >= disheight or y1 < 0:
            return 'lost', score

        snakehead = [x1, y1]
        snakelist.append(snakehead)
        if len(snakelist) > snakelength:
            del snakelist[0]

        if snakehead in snakelist[:-1]:
            return 'lost', score

        if x1 == foodx and y1 == foody:
            snakelength += 1
            foodx, foody = new_food(snakelist)

        dis.blit(bgd_image, (0, 0))
        pygame.draw.rect(dis, green, [foodx, foody, snakeblock, snakeblock])
        oursnake(snakelist)
        draw_hud(snakelength - 1, (snakelength - 1) // points_per_level + 1,
                 max(highscore, snakelength - 1))
        pygame.display.update()

        clock.tick(speed)

def main():
    highscore = load_highscore()
    if not start_screen(highscore):
        pygame.quit()
        return

    while True:
        result, score = run_game(highscore)
        new_record = score > highscore
        if new_record:
            highscore = score
            save_highscore(highscore)
        if result == 'quit':
            break
        if game_over_screen(score, highscore, new_record) == 'quit':
            break

    pygame.quit()

if __name__ == '__main__':
    main()