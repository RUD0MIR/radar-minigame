import math

import pygame
from pygame import Surface, Rect
from pygame.sprite import Group, Sprite
from pytmx.pytmx import Point
from shapely import geometry, ops


class Wall(pygame.sprite.Sprite):
    def __init__(self, rect: Rect, group: Group):
        super().__init__(group)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill('white')
        self.image.fill('#0f0f0f')


class Marker(pygame.sprite.Sprite):
    def __init__(self, rect: Rect, group: Group):
        super().__init__(group)
        self.rect = rect
        self.frames = []
        self.load_frames()
        self.anim_index = 0
        self.image = self.frames[self.anim_index]

    def load_frames(self):
        for i in range(1, 7):
            image = pygame.image.load(f'res/animated_sprite/marker/{i}.png').convert_alpha()
            smaller_image = pygame.transform.smoothscale(image, (35, 35))
            self.frames.append(smaller_image)

    def on_collide(self, player):
        if pygame.sprite.collide_rect(player, self):
            pass
            # TODO on collide

    def proceed_animation(self):
        self.anim_index += 0.12
        if self.anim_index > len(self.frames):
            self.anim_index = 0

        print(int(self.anim_index))
        self.image = self.frames[int(self.anim_index)]

    def update(self, player):
        self.proceed_animation()
        self.on_collide(player)


class Walls(pygame.sprite.Group):
    def __init__(self, surface, tmx_data):
        # self.color = (0, 0, 0, 0)
        super().__init__()
        self.surface = surface

        self.tmx_data = tmx_data
        self.get_walls_from_tmx()

    def get_walls_from_tmx(self):
        for obj in self.tmx_data.objects:
            if obj.type != 'marker':
                Wall(pygame.Rect(obj.x, obj.y, obj.width, obj.height), self)


class Markers(pygame.sprite.Group):
    def __init__(self, surface, tmx_data, player: Sprite):
        super().__init__()
        self.surface = surface
        self.player = player

        self.tmx_data = tmx_data
        self.get_markers_from_tmx()

    def get_markers_from_tmx(self):
        for obj in self.tmx_data.objects:
            if obj.type == 'marker':
                Marker(pygame.Rect(obj.x, obj.y, obj.width, obj.height), self)
