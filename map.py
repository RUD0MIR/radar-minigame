import math

import pygame
from pygame import Surface, Rect
from pygame.sprite import Group
from pytmx.pytmx import Point
from shapely import geometry, ops


class Wall(pygame.sprite.Sprite):
    def __init__(self, rect: Rect, group: Group):
        super().__init__(group)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill('white')
        self.mask = pygame.mask.from_surface(self.image)


class Walls(pygame.sprite.Group):
    def __init__(self, surface, tmx_data):
        # self.color = (0, 0, 0, 0)
        super().__init__()
        self.surface = surface
        self.color = 'white'

        self.tmx_data = tmx_data
        self.get_rects_from_tmx()
        print(len(self.sprites()))

    def get_rects_from_tmx(self):
        for obj in self.tmx_data.objects:
            Wall(pygame.Rect(obj.x, obj.y, obj.width, obj.height), self)
