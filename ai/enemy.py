import math

import pygame
from pygame import Surface, Vector2
from pygame.sprite import Group, Sprite
from shapely import Point

from ai.map import Wall, Walls
from line import Line
from ai.player import Player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_pos, player: Player, walls: Walls, group: Group, screen):  # rays: Rays
        super().__init__(group)
        self.screen = screen

        self.start_pos = start_pos
        self.size = (10, 10)
        self.fov_length = 100
        self.speed = 0.5
        self.line_to_player = None
        self.fov_line = Line((0, 0), (0, 0))
        self.direction = pygame.math.Vector2(start_pos)
        self.group = group

        self.player = player
        self.walls = walls

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image.fill('blue')  # (0,0,0,0)
        self.rect = pygame.Rect(start_pos, self.size)

        self.counter = 0
        self.previous_pos = start_pos

    def fov_collided_with_player(self, player_pos):
        return self.fov_line.is_point_on_line(player_pos)

    def collided_with_wall(self):
        return pygame.sprite.spritecollideany(self, self.walls)

    def collided_with_rays(self):
        # if pygame.sprite.spritecollideany(self, self.rays):
        self.image.fill('red')
        pass

    def set_direction(self, player_pos):
        self.line_to_player = Line(self.start_pos, player_pos)
        fov_end_point = self.line_to_player.get_point(self.fov_length)
        self.fov_line = Line(self.start_pos, fov_end_point)

        # self.direction.x = self.fov_line.x_vector_direction()
        # self.direction.y = self.fov_line.y_vector_direction()

    def test_move(self, player_pos):
        # if self.fov_collided_with_player(player_pos):

        if self.collided_with_wall():
            self.direction = self.direction.move_towards(player_pos, -self.speed * 1.5)
        else:
            self.direction = self.direction.move_towards(player_pos, self.speed)

        self.rect.x = self.direction.x
        self.rect.y = self.direction.y

    # def move_to_player(self, player_pos):
    #     if self.fov_collided_with_player(player_pos):
    #         self.start_pos = self.fov_line.get_point(self.speed)
    #         self.rect = pygame.Rect(self.start_pos, self.size)
    #
    #         if self.collided_with_wall():
    #             self.start_pos = self.fov_line.get_point(self.speed // 2)
    #             self.rect = pygame.Rect(self.start_pos, self.size)

    def update(self, player_pos):
        self.set_direction(player_pos)
        self.test_move(player_pos)
        pygame.draw.line(self.screen, 'red', self.direction, player_pos)
        pygame.draw.line(self.screen, 'blue', self.fov_line.p0, self.fov_line.p1)


class Enemies(pygame.sprite.Group):
    def __init__(self, player, walls, screen):
        super().__init__()
        self.screen = screen
        self.count = 1
        self.player = player
        self.walls = walls
        self.generate_enemies()

    def generate_enemies(self):
        for i in range(0, self.count):
            Enemy((250, 170), self.player, self.walls, self, self.screen)
