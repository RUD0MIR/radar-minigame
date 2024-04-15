import random

import pygame
from pygame import Surface
from pygame.sprite import Group

from sonar import const
from sonar.line_fov import LineFov
from sonar.map import Walls
from sonar.pathfinder import Pathfinder
from sonar.rays import RaysPulse


class Enemy(pygame.sprite.Sprite):
    def __init__(self, matrix, default_pos, patrol_points: list[tuple[int, int]], cell_size, group: Group):
        super().__init__(group)
        self.size = (cell_size, cell_size)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image.fill(const.green)
        self.rect = pygame.Rect(default_pos, self.size)
        self.group = group

        self.alpha = 0
        self.alpha_decrease_rate = 2
        self.alpha_counter = -1
        self.alpha_counter_max_value = 150

        self.image.set_alpha(self.alpha)

        self.seen_player = False

        # movement
        self.pos = self.rect.center
        self.speed = random.choice([0.7, 0.8, 0.8, 0.9])
        self.patrol_points = patrol_points
        self.moving_forward_on_patrol = True

        # fov
        self.fov = LineFov(200)

        # pathfinding
        self.path_modifier = random.uniform(-5, 5)
        self.pathfinder = Pathfinder(cell_size, matrix, self.fov.radius, self.path_modifier)
        self.pathfinding_counter = 0

    def follow_player(self, player_pos):
        self.pos += self.pathfinder.direction * self.speed

        self.rect.center = self.pos
        self.pathfinder.check_path_points_collision(self.pos)

        if self.pathfinding_counter > 10:
            self.pathfinding_counter = 0
        if self.pathfinding_counter == 10:
            self.pathfinder.find_path(
                (self.rect.centerx, self.rect.centery),
                player_pos
            )

        self.pathfinder.get_direction(self.pos)
        self.pathfinding_counter += 1

    def follow_patrol(self):
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

    def animate_alpha(self, rays_pulses):
        for ray_pulse in rays_pulses:
            if pygame.sprite.spritecollideany(self, ray_pulse):
                self.alpha_counter = 0
                self.alpha = 255

        if self.alpha_counter >= self.alpha_counter_max_value:
            self.alpha_counter = 0
            self.alpha = 0
            return

        self.alpha -= self.alpha_decrease_rate
        self.alpha_counter += 1
        self.image.set_alpha(self.alpha)

    def update(self, player_pos, screen: Surface, rays: RaysPulse, walls: Walls):
        self.animate_alpha(rays)
        self_pos = self.rect.centerx, self.rect.centery

        if self.seen_player or not self.fov.fov_line_blocked_by_wall(self_pos, player_pos, walls):
            if not self.fov.radius_exceeded(self_pos, player_pos):
                self.seen_player = True
                self.follow_player(player_pos)
        else:
            self.follow_patrol()

        # fov and pathfinding debug stuff
        # self.fov.draw_fov_line(screen, walls)
        # self.pathfinder.draw_path(screen)


class Enemies(pygame.sprite.Group):
    def __init__(self, matrix, cell_size):
        super().__init__()
        self.matrix = matrix
        self.cell_size = cell_size
        self.en_positions = [
            (26 * cell_size, 85 * cell_size),
            (68 * cell_size, 53 * cell_size),
            # (41 * 10, 22 * 10)
        ]
        self.en_patrol_points = [
            [(45 * cell_size, 82 * cell_size), (69 * cell_size, 73 * cell_size)],
            [(55 * cell_size, 38 * cell_size), (94 * cell_size, 52 * cell_size)]
        ]

        self.generate_enemies()

    def generate_enemies(self):
        for i in range(len(self.en_positions)):
            Enemy(self.matrix, self.en_positions[i], self.en_patrol_points[i], self.cell_size, self)
