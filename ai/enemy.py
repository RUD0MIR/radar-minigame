import math

import pygame
from pygame import Surface, Vector2
from pygame.sprite import Group, Sprite
from shapely import Point

from line import Line
from ai.player import Player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos, player: Player):
        super().__init__()
        self.start_pos = start_pos
        self.size = (600, 500)
        self.fov_length = 150
        self.speed = 1
        self.fov_line = None

        self.player = player

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    # def collided_with_player(self, player_pos):
    #
    #
    #     return cross == 0
    #
    # def move_to_player(self, player_pos):
    #     if self.collided_with_player(player_pos):
    #         self.start_pos = self.get_line_point(self.start_pos, player_pos, self.speed)

    def update(self, player_pos):
        self.fov_line = Line(self.start_pos, player_pos)
        # self.move_to_player(player_pos)
        end_point = self.fov_line.get_point(self.fov_length)

        self.image.fill((0, 0, 0, 0))
        pygame.draw.line(self.image, (255, 0, 0, 50), self.start_pos, end_point, width=10)
        pygame.draw.rect(self.image, 'blue', (self.start_pos, (10, 10)))
