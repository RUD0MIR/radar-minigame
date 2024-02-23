import itertools
import math
import multiprocessing
from operator import itemgetter

import pygame
from pygame import Surface
from pygame.sprite import Group


class Ray(pygame.sprite.Sprite):
    def __init__(self, surface: Surface, start_pos, angle, group: Group, walls: Group):
        super().__init__(group)
        self.surface = surface

        self.start_pos = start_pos
        self.len = 0
        self.angle = angle
        self.end_pos = (self.start_pos[0] + self.len * math.cos(self.angle), self.start_pos[1] + self.len * math.sin(self.angle))

        self.walls = walls

        self.rect = pygame.draw.line(self.surface, 'red', self.start_pos, self.end_pos)
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)

    '''
    calculating ray end point with these formulas
    x = x0 + R * cos(a)
    y = y0 + R * sin(a)
    '''
    # def calculate_end_pos(self):
    #     x =
    #     y =
    #     self.end_pos = x, y

    def update(self):

        if not pygame.sprite.spritecollideany(self, self.walls):
            self.len += 1
            self.end_pos = (
                self.start_pos[0] + self.len * math.cos(self.angle), self.start_pos[1] + self.len * math.sin(self.angle)
            )
        else:
            pygame.draw.rect(self.surface, 'red', (self.end_pos, (5, 5)))
        self.rect = pygame.draw.line(self.surface, 'red', self.start_pos, self.end_pos)


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
            Ray(self.surface, self.start_pos, i, self, self.walls)

    def draw(self, surface, bgsurf=None, special_flags=0):
        for sprite in self.sprites():
            self.surface.blit(sprite.image, sprite.rect)
