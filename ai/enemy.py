import random

import pygame
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pygame import Surface
from pygame.sprite import Group
from shapely import Point

from ai.map import Walls, test_pathfinding_grid
from ai.pathfinder import Pathfinder
from ai.player import Player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, default_pos, walls: Walls, group: Group):

        # basic
        super().__init__(group)
        self.size = (10, 10)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image.fill('blue')
        self.rect = pygame.Rect(default_pos, self.size)
        self.group = group

        self.fov_radius = 20
        self.seen_player = False
        self.walls = walls

        # movement
        self.pos = self.rect.center
        self.actual_speed = 0
        self.speed_const = random.choice([0.7, 0.8, 0.8, 0.9])

        # path
        self.path_modifier = random.uniform(-5, 5)
        self.pathfinder = Pathfinder(10, test_pathfinding_grid, self.fov_radius, self.path_modifier)

        self.pathfinding_counter = 0

    def fov_line_blocked_by_wall(self):
        if self.pathfinder.path:
            points = []
            for point in self.pathfinder.path:
                x = (point.x * self.pathfinder.cell_size) + self.pathfinder.cell_size // 2
                y = (point.y * self.pathfinder.cell_size) + self.pathfinder.cell_size // 2
                points.append((x, y))

            line = (points[0], points[-1])
            return any(wall.rect.clipline(line) for wall in self.walls)

    def draw_fov_line(self, screen):
        if self.pathfinder.path:
            points = []
            for point in self.pathfinder.path:
                x = (point.x * self.pathfinder.cell_size) + self.pathfinder.cell_size // 2
                y = (point.y * self.pathfinder.cell_size) + self.pathfinder.cell_size // 2
                points.append((x, y))

            fov_line = (points[0], points[-1])
            color = "red" if any(wall.rect.clipline(fov_line) for wall in self.walls) else "green"
            pygame.draw.line(screen, color, fov_line[0], fov_line[1])

    def follow_path(self, player):
        if self.fov_line_blocked_by_wall() == False or self.seen_player:
            self.actual_speed = self.speed_const
            self.seen_player = True

        self.pos += self.pathfinder.direction * self.actual_speed

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

    def update(self, player: Player, screen: Surface):
        self.follow_path(player)
        # self.draw_fov_line(screen)
        # self.pathfinder.draw_path(screen)


class Enemies(pygame.sprite.Group):
    def __init__(self, matrix, walls: Walls):
        super().__init__()
        self.matrix = matrix
        self.walls = walls
        self.en_positions = [
            (45 * 10, 33 * 10),
            (40 * 10, 26 * 10),
            (41 * 10, 22 * 10)
        ]
        self.en_default_paths = [

            [Point(6, 29), Point(1, 29)]
        ]

        self.generate_enemies()

    def generate_enemies(self):
        for i in range(len(self.en_positions)):
            Enemy(self.en_positions[i], self.walls, self)
