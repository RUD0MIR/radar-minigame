import math

import pygame
from pygame.sprite import Group

from sonar import const
from sonar.map import Walls


class Ray(pygame.sprite.Sprite):
    def __init__(self, start_pos, angle, group: Group, walls: Walls, hit_color, max_len):
        super().__init__(group)
        self.start_pos = start_pos
        self.angle = angle
        self.collided = False
        self.max_len = max_len
        self.def_color = const.black
        self.hit_color = hit_color
        self.alpha = 360
        self.alpha_decrease_rate = 2.5
        self.walls = walls
        self.rect = pygame.Rect(start_pos[0], start_pos[1], 3, 3)
        self.image = pygame.Surface(
            (self.rect.width, self.rect.height)
        )
        self.image.fill(self.def_color)

    def move_rect(self, ray_len):
        """
        moves ray rect along a linear trajectory, which is calculated by the formulas:
        x = x0 + R * cos(a)
        y = y0 + R * sin(a)
        """
        rect_pos = (
            self.start_pos[0] + ray_len * math.cos(self.angle), self.start_pos[1] + ray_len * math.sin(self.angle)
        )
        self.rect = pygame.Rect(rect_pos[0], rect_pos[1], 3, 3)

    def fade_image(self):
        self.alpha -= self.alpha_decrease_rate
        self.image.fill(self.hit_color)
        self.image.set_alpha(self.alpha)

    def update(self, ray_len):
        if self.alpha <= 0 or (not self.collided and ray_len >= self.max_len):
            self.kill()

        if self.collided or pygame.sprite.spritecollideany(self, self.walls):
            self.fade_image()
            self.collided = True
        else:
            self.move_rect(ray_len)


class RaysPulse(pygame.sprite.Group):
    def __init__(self, player_pos, walls, color):
        super().__init__()
        self.walls = walls
        self.rays_max_length = 470
        self.nearby_walls = walls.get_nearby_walls(player_pos, self.rays_max_length)

        self.rays_count = 220
        self.rays_len = 0
        self.rays_speed = 6
        self.color = color

        self.generate_rays(player_pos)

    def generate_rays(self, player_pos):
        self.rays_len = 0
        self.nearby_walls = self.walls.get_nearby_walls(player_pos, self.rays_max_length)
        for i in range(self.rays_count):
            Ray(player_pos, i, self, self.nearby_walls, self.color, self.rays_max_length)

    def custom_update(self, player_pos):
        if len(self.sprites()) == 0:
            self.generate_rays(player_pos)

        self.rays_len += self.rays_speed
        for ray in self.sprites():
            ray.update(self.rays_len)
