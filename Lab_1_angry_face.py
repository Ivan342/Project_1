import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

background = GRAY
screen.fill(background)

pygame.draw.ellipse(screen, YELLOW, (50, 50, 300, 300))
pygame.draw.ellipse(screen, BLACK, (50, 50, 300, 300), 3)
pygame.draw.ellipse(screen, RED, (100, 145, 55, 55))
pygame.draw.ellipse(screen, BLACK, (100, 145, 55, 55), 2)
pygame.draw.ellipse(screen, RED, (240, 155, 50, 50))
pygame.draw.ellipse(screen, BLACK, (240, 155, 50, 50), 2)

pygame.draw.ellipse(screen, BLACK, (100+55/2-30/2, 145+55/2-30/2, 30, 30))
pygame.draw.ellipse(screen, BLACK, (240+50/2-25/2, 155+50/2-25/2, 25, 25))

pygame.draw.rect(screen, BLACK, (120, 270, 160, 30))

line(screen, BLACK, (60, 60), (160, 150), 30)
line(screen, BLACK, (360, 60), (240, 150), 30)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
