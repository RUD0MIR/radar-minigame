from pygame.locals import *
import pygame
import sys
from pytmx import load_pygame

from camera import CameraGroup
from map import Wall, Walls, Markers
from player import Player
from rays import Rays
from sonar.enemy import Enemies
from sonar.res.cave import matrix


# TODO add rays to camera
class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.running = True
        self.debug = False

        # drawing related stuff
        self.colors = {
            'text': (231, 111, 81),
            'background': '#0f0f0f',
            'player': (244, 162, 97)
        }

        self.font = pygame.font.SysFont('Arial', 20)

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.screen_width, self.screen_height = 1920, 1080
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_dimensions)

        # self.render_width, self.render_height = 1920, 1080
        # self.render_dimensions = (self.render_width, self.render_height)
        # self.render_surface = pygame.Surface(self.render_dimensions)

        # ground
        # self.ground_surf = pygame.image.load('graphics/ground.png').convert_alpha()
        # self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))
        self.kpk = pygame.image.load(f"res/kpk.png").convert_alpha()

        # objects
        tmx_map = load_pygame("res/cave_tiled.tmx")
        self.walls = Walls(self.screen, tmx_map)

        self.camera_group = CameraGroup()

        print(matrix.cave_grid)

        self.enemies = Enemies(matrix.cave_grid, 10)

        self.initial_player_position = [60, 840]
        self.player = Player(self.initial_player_position, self.walls, self.enemies, self.camera_group)

        self.map_graphics = Markers(self.screen, tmx_map, self.player)
        # TODO optimize rays
        self.rays = Rays(self.screen, self.initial_player_position, self.walls)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()

            self.draw()
            self.update()

    def draw(self):
        self.camera_group.custom_draw(self.player, [self.walls, self.map_graphics, self.rays, self.enemies])

        self.screen.blit(
            self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, self.colors['text']), (5, 5)
        )

    def update(self):
        self.map_graphics.update(self.player)
        self.camera_group.update()
        self.enemies.update(self.player, self.screen, self.walls)
        self.rays.custom_update(self.player.rect.center)

        pygame.display.update()
        self.screen.fill(self.colors['background'])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


if __name__ == '__main__':
    app = Game()
    app.run()
