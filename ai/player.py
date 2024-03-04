import math

import pygame
from pygame.sprite import Group


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, new_pos):
        self.rect = self.image.get_rect(center=new_pos)


