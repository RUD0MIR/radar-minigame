import random

import pygame
from pygame import Surface
from pygame.sprite import Group

from ai.line_fov import LineFov
from ai.map import Walls, test_pathfinding_grid
from ai.pathfinder import Pathfinder
from ai.player import Player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, default_pos, patrol_points: list[tuple[int, int]], cell_size, group: Group):

        # basic
        super().__init__(group)
        self.size = (cell_size, cell_size)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image.fill('blue')
        self.rect = pygame.Rect(default_pos, self.size)
        self.group = group

        self.seen_player = False

        # movement
        self.pos = self.rect.center
        self.speed = random.choice([0.7, 0.8, 0.8, 0.9])
        self.patrol_points = patrol_points
        self.moving_forward_on_patrol = True

        # fov
        self.fov = LineFov(150)

        # path
        self.path_modifier = random.uniform(-5, 5)
        self.pathfinder = Pathfinder(cell_size, test_pathfinding_grid, self.fov.radius, self.path_modifier)
        self.pathfinding_counter = 0

    def follow_player(self, player, walls: Walls):
        self.pos += self.pathfinder.direction * self.speed

        self.rect.center = self.pos
        self.pathfinder.check_path_points_collision(self.pos)

        if self.pathfinding_counter > 10:
            self.pathfinding_counter = 0

        if self.pathfinding_counter == 10:
            self.pathfinder.find_path(
                (self.rect.centerx, self.rect.centery),
                (player.rect.centerx, player.rect.centery)
            )

        self.pathfinder.get_direction(self.pos)

        self.pathfinding_counter += 1

    def follow_patrol(self, walls: Walls, player_pos):
        self.pos += self.pathfinder.direction * self.speed
        self.rect.center = self.pos
        if self.pathfinder.check_path_points_collision(self.pos):
            self.moving_forward_on_patrol = not self.moving_forward_on_patrol
        if self.pathfinding_counter > 10:
            self.pathfinding_counter = 0
        if self.pathfinding_counter == 10:
            self.pathfinder.find_path(
                (self.rect.centerx, self.rect.centery),
                self.patrol_points[0] if self.moving_forward_on_patrol else self.patrol_points[1]
            )
        self.pathfinder.get_direction(self.pos)
        self.pathfinding_counter += 1

    def update(self, player: Player, screen: Surface, walls: Walls):
        self_pos = self.rect.centerx, self.rect.centery
        player_pos = player.rect.centerx, player.rect.centery
        if self.seen_player or self.fov.fov_line_blocked_by_wall(self_pos, player_pos, walls) == False:
            self.seen_player = True
            if not self.fov.radius_exceeded(self_pos, player_pos):
                self.follow_player(player, walls)
        else:
            self.follow_patrol(walls, player_pos)
        # self.fov.draw_fov_line(screen, walls)


class Enemies(pygame.sprite.Group):
    def __init__(self, matrix, cell_size):
        super().__init__()
        self.matrix = matrix
        self.cell_size = cell_size
        self.en_positions = [
            (45 * cell_size, 33 * cell_size),
            # (40 * 10, 26 * 10),
            # (41 * 10, 22 * 10)
        ]
        self.en_default_paths = [
            [(36 * cell_size, 20 * cell_size), (49 * cell_size, 38 * cell_size)]
        ]

        self.generate_enemies()

    def generate_enemies(self):
        for i in range(len(self.en_positions)):
            Enemy(self.en_positions[i], self.en_default_paths[i], self.cell_size, self)
