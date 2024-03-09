from pygame.locals import *
import pygame
import sys
from pytmx import load_pygame, TiledMap

from ai.map import Walls, test_pathfinding_grid
from ai.enemy1 import Enemy1
from enemy import Enemy, Enemies
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        # pygame.mouse.set_visible(False)

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

        # tmx_map = load_pygame("ai_test_map.tmx")
        tmx_map = load_pygame("ai_pathfinding_tilemap.tmx")
        self.walls = Walls(self.screen, tmx_map)

        self.player = Player((500, 300), self.walls)

        # self.enemies = Enemies(self.player, self.walls, self.screen)
        self.enemy = Enemy1(test_pathfinding_grid, (50, 280))

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()

            self.screen.blit(
                self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, self.colors['text']), (5, 5)
            )

            self.screen.blit(self.enemy.image, self.enemy.rect)
            self.enemy.update()
            self.enemy.draw_path(self.screen)

            self.walls.draw(self.screen)
            self.walls.update()

            # self.enemies.draw(self.screen)
            # self.enemies.update((self.player.rect.x, self.player.rect.y))

            # self.screen.blit(self.player.image, self.player.rect)
            # self.player.update(pygame.mouse.get_pos())

            pygame.display.update()
            self.screen.fill(self.colors['background'])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.enemy.find_path()



if __name__ == '__main__':
    app = Game()
    app.run()
