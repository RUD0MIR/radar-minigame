import pygame
from pytmx import load_pygame

from camera import CameraGroup
from map import Walls
from player import Player
from rays import RaysPulse
from sonar import const
from sonar.enemy import Enemies
from util.util import invert_binary_matrix


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.running = True
        self.debug = False

        self.font = pygame.font.SysFont('Arial', 20)

        self.fps = 60
        self.clock = pygame.time.Clock()

        self.screen_width, self.screen_height = 1920, 1080
        self.screen_dimensions = (self.screen_width, self.screen_height)
        self.screen = pygame.display.set_mode(self.screen_dimensions)

        self.kpk = pygame.image.load(f"res/kpk.png").convert_alpha()

        # TMX from Tiled
        walls_layer = load_pygame("res/cave_tiled.tmx").layers[0]
        # markers_layer = load_pygame("res/cave_tiled.tmx").layers[1]
        cell_size = 10
        matrix = invert_binary_matrix(load_pygame("res/cave_tiled.tmx").layers[0].data)

        self.walls = Walls(self.screen, walls_layer, cell_size)

        self.camera_group = CameraGroup()

        self.enemies = Enemies(matrix, cell_size)

        self.player = Player(self.walls, self.enemies, self.camera_group)

        # self.map_graphics = Markers(self.screen, markers_layer, self.player)
        self.rays_pulses = [
            RaysPulse(self.player.rect.center, self.walls, const.dark_green),
            RaysPulse(self.player.rect.center, self.walls, 'red')
        ]

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()

            self.draw()
            self.update()

    def draw(self):
        self.camera_group.custom_draw(
            self.player,
            [self.walls, self.rays_pulses[0], self.rays_pulses[1], self.enemies]
        )

        self.screen.blit(
            self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, 'orange'), (5, 5)
        )

    def update(self):
        # self.map_graphics.update(self.player)
        self.camera_group.update()
        self.enemies.update(self.player, self.screen, self.rays_pulses, self.walls)
        self.rays_pulses[0].custom_update(self.player.rect.center)

        pygame.display.update()
        self.screen.fill(const.black)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


if __name__ == '__main__':
    app = Game()
    app.run()
