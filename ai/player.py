import math

import pygame
from pygame.sprite import Group


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, walls):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.direction = pygame.math.Vector2()
        self.speed = 4#1

        self.walls = walls

    def map_collide_with_player(self):
        return pygame.sprite.spritecollideany(self, self.walls)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self):
        self.rect.x += self.direction.x * self.speed
        if self.map_collide_with_player():
            if self.direction.x > 0:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

        self.rect.y += self.direction.y * self.speed
        if self.map_collide_with_player():
            if self.direction.y > 0:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

    def update(self, new_pos):
        self.move()
        self.input()


