import pygame

from camera import CameraGroup
from map import Walls
from player import Player
from rays import RaysPulse
from sonar import const
from sonar.enemy import Enemies
from sonar.level import Level


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

        self.kpk = pygame.image.load(f"res/img/kpk.png").convert_alpha()

        matrix_cell_size = 20

        # Levels
        self.floo1 = Level((22 * matrix_cell_size, 20 * matrix_cell_size), "res/maps/1floor.tmx")
        self.current_map = self.floo1

        # Game objects
        self.walls = Walls(self.screen, self.current_map.walls_layer, matrix_cell_size)
        self.camera_group = CameraGroup()
        self.enemies = Enemies(self.current_map.matrix, matrix_cell_size)
        self.player = Player(
            (10, 10),
            self.current_map.player_spawn_pos,
            self.walls,
            self.enemies, self.camera_group
        )
        self.rays_pulses = [
            RaysPulse(self.player.rect.center, self.walls, const.dark_green),
            RaysPulse(self.player.rect.center, self.walls, const.dark_green)
        ]
        self.second_ray_pulse_delay_counter = 0
        self.second_ray_pulse_delay = 90

    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_input()
            self.draw()
            self.update()

    def draw(self):
        # draw all objects from camera class
        self.camera_group.custom_draw(
            self.player.rect,
            [self.walls, self.rays_pulses[0], self.rays_pulses[1], self.enemies]
        )

        # in game fps display
        self.screen.blit(
            self.font.render('fps: ' + str(round(self.clock.get_fps(), 2)), True, 'orange'), (5, 5)
        )

    def update(self):
        self.camera_group.update()
        # self.enemies.update(self.player.rect.center, self.screen, self.rays_pulses, self.walls)
        self.rays_pulses[0].custom_update(self.player.rect.center)
        self.walls.update(self.rays_pulses)

        # updating second RayPulse after delay, so they are not simultaneous
        if self.second_ray_pulse_delay_counter > self.second_ray_pulse_delay:
            self.rays_pulses[1].custom_update(self.player.rect.center)
        if self.second_ray_pulse_delay_counter <= self.second_ray_pulse_delay:
            self.second_ray_pulse_delay_counter += 1

        pygame.display.update()
        self.screen.fill(const.black)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


if __name__ == '__main__':
    app = Game()
    app.run()
