from pygame.locals import *
import pygame
import sys
from pytmx import load_pygame

from camera import CameraGroup
from map import Wall, Walls, Markers
from player import Player
from rays import Rays


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
        tmx_map = load_pygame("res/cave.tmx")
        self.walls = Walls(self.screen, tmx_map)

        self.camera_group = CameraGroup()

        self.initial_player_position = [220, 1000]
        self.player = Player(self.initial_player_position, self.walls, self.camera_group)

        self.map_graphics = Markers(self.screen, tmx_map, self.player)
        self.rays = Rays(self.screen, self.initial_player_position, self.walls)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()
            self.rays.custom_update(self.player.rect)
            self.map_graphics.update(self.player)

            self.camera_group.update()
            self.camera_group.custom_draw(self.player, [self.walls, self.rays, self.map_graphics])

            self.screen.blit(
                self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, self.colors['text']), (5, 5)
            )
            # self.screen.blit(pygame.transform.scale(self.render_surface, self.screen_dimensions), (0, 0))
            pygame.display.update()
            self.screen.fill(self.colors['background'])

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


if __name__ == '__main__':
    app = Game()
    app.run()
