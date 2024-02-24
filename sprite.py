import math

import pygame
from pygame.sprite import Group


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, walls: Group, group: Group):
        super().__init__(group)
        self.image = pygame.Surface((10, 10))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)

        self.direction = pygame.math.Vector2()
        self.speed = 1

        self.walls = walls

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

    # TODO add exit mechanic
    def on_exit(self):
        pass

    def exits_collide_with_player(self):
        pass

    # TODO add exit mechanic

    def map_collide_with_player(self):
        return pygame.sprite.spritecollideany(self, self.walls)

    def update(self):
        self.on_exit()
        self.move()
        self.input()


class Ray(pygame.sprite.Sprite):
    def __init__(self, start_pos, angle, group: Group, walls: Group):
        super().__init__(group)

        self.start_pos = start_pos
        self.len = 0
        self.angle = angle
        self.rect_pos = start_pos

        self.walls = walls

        self.rect = pygame.Rect(self.rect_pos[0], self.rect_pos[1], 3, 3)
        self.image = pygame.Surface(
            (self.rect.width, self.rect.height)  # , pygame.SRCALPHA
        )
        self.image.fill('green')

    '''
    calculating ray end point with these formulas
    x = x0 + R * cos(a)
    y = y0 + R * sin(a)
    '''

    def move_rect(self):
        self.len += 1
        self.rect_pos = (
            self.start_pos[0] + self.len * math.cos(self.angle), self.start_pos[1] + self.len * math.sin(self.angle)
        )

        self.rect = pygame.Rect(self.rect_pos[0], self.rect_pos[1], 3, 3)

    def update(self):
        if pygame.sprite.spritecollideany(self, self.walls):
            self.image.fill('red')
        else:
            self.move_rect()
