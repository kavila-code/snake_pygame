import pygame
pygame.init()

# 01_image.png: carita amarilla sobre fondo rosado (255, 0, 255)
img = pygame.Surface((64, 64))
img.fill((255, 0, 255))
pygame.draw.circle(img, (255, 255, 0), (32, 32), 30)
pygame.draw.circle(img, (0, 0, 0), (22, 24), 5)
pygame.draw.circle(img, (0, 0, 0), (42, 24), 5)
pygame.draw.arc(img, (0, 0, 0), (16, 24, 32, 24), 3.4, 6.0, 3)
pygame.image.save(img, '01_image.png')

# background.png: baldosas grises
bg = pygame.Surface((600, 400))
bg.fill((170, 170, 170))
for x in range(0, 600, 20):
    pygame.draw.line(bg, (60, 60, 60), (x, 0), (x, 400), 2)
for y in range(0, 400, 20):
    pygame.draw.line(bg, (60, 60, 60), (0, y), (600, y), 2)
pygame.image.save(bg, 'background.png')

print('Listo: se crearon 01_image.png y background.png')