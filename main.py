from pygame.locals import *
from operator import add, sub
import pygame
import sys
import math
import random

from pytmx import load_pygame

from map import Map, Line
from rays import Rays

pygame.init()

# -----Options-----
WINDOW_SIZE = (1920, 1080)  # Width x Height in pixels
NUM_RAYS = 150  # Must be between 1 and 360
SOLID_RAYS = False  # Can be somewhat glitchy. For best results, set NUM_RAYS to 360
NUM_WALLS = 5  # The amount of randomly generated walls
# ------------------

screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


running = True
# walls = []





# def generateWalls():
#     walls.clear()
#
#     walls.append(Wall((0, 0), (WINDOW_SIZE[0], 0)))
#     walls.append(Wall((0, 0), (0, WINDOW_SIZE[1])))
#     walls.append(Wall((WINDOW_SIZE[0], 0), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
#     walls.append(Wall((0, WINDOW_SIZE[1]), (WINDOW_SIZE[0], WINDOW_SIZE[1])))
#
#     for i in range(NUM_WALLS):
#         start_x = random.randint(0, WINDOW_SIZE[0])
#         start_y = random.randint(0, WINDOW_SIZE[1])
#         end_x = random.randint(0, WINDOW_SIZE[0])
#         end_y = random.randint(0, WINDOW_SIZE[1])
#         walls.append(Wall((start_x, start_y), (end_x, end_y)))


_map = Map(load_pygame("sonar_sample_map.tmx"), screen)
rays = Rays(_map.lines, screen)


def draw():
    screen.fill((0, 0, 0))

    _map.draw_lines()
    rays.draw_rays()

    pygame.display.update()


# generateWalls()

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    rays.update(mouse_pos)

    draw()
    clock.tick(60)
