from pygame.locals import *
import pygame
import sys
from pytmx import load_pygame

from map import Wall, Walls
from sprite import Player
from sprite_group import CameraGroup, Rays


# TODO remove cringe rays
# TODO send rects along a linear trajectory, in case of collision, show them

# TODO add camera, player and collision for player
class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.running = True
        self.debug = False

        # drawing related stuff
        self.colors = {
            'text': (231, 111, 81),
            'background': (0, 0, 0),
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
        self.walls = Walls(self.screen, load_pygame("res/testMap1.tmx"))

        self.camera_group = CameraGroup()

        self.player_position = [1920 // 2, 1080 // 2]
        self.player = Player(self.player_position, self.walls, self.camera_group)

        self.rays = Rays(self.screen, self.player_position, self.walls)

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()

            # self.walls.draw(self.render_surface)
            self.rays.draw(self.screen)
            self.rays.update()

            self.camera_group.update()
            self.camera_group.custom_draw(self.player, self.walls)
            # self.walls.update()

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
