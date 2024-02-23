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
        self.len = 1000
        self.angle = 10#angle
        self.end_pos = (
            self.start_pos[0] + 100, self.start_pos[1] + 100
        )
        #self.start_pos[0] + self.len * math.cos(self.angle), self.start_pos[1] + self.len * math.sin(self.angle)

        self.walls = walls

        self.image = pygame.Surface(
            (100, 100), pygame.SRCALPHA
        )
        self.image.fill('white')
        pygame.draw.line(self.image, 'red',(0,0), (100, 100))# self.start_pos, self.end_po

        #abs(self.end_pos[0] - self.start_pos[0]), abs(self.end_pos[1]  -  self.start_pos[1]))
        self.rect = pygame.Rect(0, 0, 1920, 1080)
        self.mask = pygame.mask.from_surface(self.image)

    '''
    calculating ray end point with these formulas
    x = x0 + R * cos(a)
    y = y0 + R * sin(a)
    '''

    def update(self):
        if pygame.sprite.spritecollideany(self, self.walls):
            if pygame.sprite.spritecollideany(self, self.walls, pygame.sprite.collide_mask):
                pygame.draw.rect(Surface((5, 5)), 'red', (self.end_pos, (5, 5)))
        else:
            pass
        self.len += 1
        self.end_pos = (
            self.start_pos[0] + self.len * math.cos(self.angle), self.start_pos[1] + self.len * math.sin(self.angle)
        )


class Rays(pygame.sprite.Group):
    def __init__(self, surface, start_pos, walls):
        super().__init__()
        self.surface = surface
        self.start_pos = start_pos
        self.rays = []
        self.walls = walls
        self.rays_color = 'white'
        self.rays_count = 1
        self.generate_rays()

    def generate_rays(self):
        for i in range(self.rays_count):
            Ray(self.start_pos, i, self, self.walls)

    def draw( self, surface, bgsurf=None, special_flags=0):
        for sprite in self.sprites():
            surface.blit(sprite.image, sprite.rect)
