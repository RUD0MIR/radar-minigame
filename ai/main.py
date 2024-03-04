from pygame.locals import *
import pygame
import sys
from pytmx import load_pygame

from enemy import Enemy
from sonar.camera import CameraGroup
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.running = True

        # drawing related stuff
        self.colors = {
            'text': (231, 111, 81),
            'background': '#0f0f0f',
            'player': (244, 162, 97)
        }

        self.font = pygame.font.SysFont('Arial', 20)

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.screen_width, self.screen_height = 600, 500
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_dimensions)

        self.player = Player((500, 300))
        self.enemy = Enemy((600 // 2, 500 // 2), self.player)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()

            self.screen.blit(
                self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, self.colors['text']), (5, 5)
            )

            self.screen.blit(self.enemy.image, self.enemy.rect)
            self.enemy.update((self.player.rect.x, self.player.rect.y))

            self.screen.blit(self.player.image, self.player.rect)
            self.player.update(pygame.mouse.get_pos())

            pygame.display.update()
            self.screen.fill(self.colors['background'])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


if __name__ == '__main__':
    app = Game()
    app.run()