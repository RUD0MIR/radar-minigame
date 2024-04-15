import math

import pygame
from pygame.sprite import Group


class Player(pygame.sprite.Sprite):
    def __init__(self, size, spawn_pos, walls: Group, enemies: Group, group: Group):
        super().__init__(group)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=spawn_pos)

        self.direction = pygame.math.Vector2()
        self.speed = 1

        self.enemies = enemies
        self.walls = walls

    def handle_input(self):
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
        if self.collide_with_walls():
            if self.direction.x > 0:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

        self.rect.y += self.direction.y * self.speed
        if self.collide_with_walls():
            if self.direction.y > 0:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

    # TODO add exit mechanic
    def on_exit(self):
        pass

    def exits_collide_with_player(self):
        pass

    # TODO add exit mechanic

    def collide_with_walls(self):
        return pygame.sprite.spritecollideany(self, self.walls)

    def collide_with_enemy(self):
        # TODO collide_with_enemy
        pass

    def update(self):
        self.collide_with_enemy()
        self.on_exit()
        self.move()
        self.handle_input()


