import itertools
import math
import multiprocessing
from operator import itemgetter

import pygame
from pygame import Surface
from pygame.sprite import Group


class Ray(pygame.sprite.Sprite):
    def __init__(self, start_pos, angle, group: Group, walls: Group):
        super().__init__(group)

        self.start_pos = start_pos
        self.len = 0
        self.angle = angle
        self.rect_pos = start_pos

        self.walls = walls

        self.rect = pygame.Rect(self.rect_pos[0], self.rect_pos[1], 3, 3)
        self.image = pygame.Surface(
            (self.rect.width, self.rect.height)  # , pygame.SRCALPHA
        )
        self.image.fill('green')

    '''
    calculating ray end point with these formulas
    x = x0 + R * cos(a)
    y = y0 + R * sin(a)
    '''
    def move_rect(self):
        self.len += 1
        self.rect_pos = (
            self.start_pos[0] + self.len * math.cos(self.angle), self.start_pos[1] + self.len * math.sin(self.angle)
        )

        self.rect = pygame.Rect(self.rect_pos[0], self.rect_pos[1], 3, 3)

    def update(self):
        if pygame.sprite.spritecollideany(self, self.walls):
            self.image.fill('red')
        else:
            self.move_rect()


class Rays(pygame.sprite.Group):
    def __init__(self, surface, start_pos, walls):
        super().__init__()
        self.surface = surface
        self.start_pos = start_pos
        self.rays = []
        self.walls = walls
        self.rays_color = 'white'
        self.rays_count = 360
        self.generate_rays()

    def generate_rays(self):
        for i in range(self.rays_count):
            Ray(self.start_pos, i, self, self.walls)
