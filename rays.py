import math

import pygame
from pygame.sprite import Group


class Ray(pygame.sprite.Sprite):
    def __init__(self, start_pos, angle, group: Group, walls: Group):
        super().__init__(group)

        self.start_pos = start_pos
        self.angle = angle
        self.rect_pos = start_pos
        self.def_color = '#0f0f0f'
        self.hit_color = '#6a8534'
        self.alpha = 255

        self.walls = walls

        self.rect = pygame.Rect(self.rect_pos[0], self.rect_pos[1], 3, 3)
        self.image = pygame.Surface(
            (self.rect.width, self.rect.height)
        )
        self.image.fill(self.def_color)

    '''
    calculating ray end point with these formulas
    x = x0 + R * cos(a)
    y = y0 + R * sin(a)
    '''

    def move_rect(self, ray_len):
        self.rect_pos = (
            self.start_pos[0] + ray_len * math.cos(self.angle), self.start_pos[1] + ray_len * math.sin(self.angle)
        )

        self.rect = pygame.Rect(self.rect_pos[0], self.rect_pos[1], 3, 3)

    def fade_image(self):
        self.alpha -= 3
        self.image.fill(self.hit_color)
        self.image.set_alpha(self.alpha)

    def update(self, ray_len):
        if pygame.sprite.spritecollideany(self, self.walls):
            self.fade_image()
        else:
            self.move_rect(ray_len)


class Rays(pygame.sprite.Group):
    def __init__(self, surface, player_pos, walls):
        super().__init__()
        self.surface = surface

        self.walls = walls

        self.rays_count = 360
        self.rays_len = 0
        self.generate_rays(player_pos)

    def generate_rays(self, player_pos):
        for i in range(self.rays_count):
            Ray(player_pos, i, self, self.walls)

    def custom_update(self, player_pos):
        if self.rays_len >= 400:
            if len(self.sprites()) == self.rays_count * 2:
                for i in range(self.rays_count):
                    self.remove(self.sprites()[i])
            self.rays_len = 0
            self.generate_rays(player_pos)

        else:
            self.rays_len += 4
            for ray in self.sprites():
                ray.update(self.rays_len)
