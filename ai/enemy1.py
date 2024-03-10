import pygame
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.core.node import GridNode
from pathfinding.finder.a_star import AStarFinder

from ai.map import Walls
from ai.player import Player


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, matrix, default_pos, walls: Walls, screen):

        # basic
        super().__init__()
        self.cell_size = 10
        self.size = (10, 10)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.image.fill('blue')
        self.rect = pygame.Rect(default_pos, self.size)

        self.fov_radius = 20
        self.walls = walls
        self.screen = screen

        # movement
        self.pos = self.rect.center
        self.speed = 0.5
        self.direction = pygame.math.Vector2(0, 0)

        # path
        self.path = []
        self.path_points = []

        # pathfinding
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)

    def empty_path(self):
        self.path = []

    @staticmethod
    def calculate_h_value(start, end):
        return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5

    #TODO ->
    def intersect_walls(self):
        if self.path:
            points = []
            for point in self.path:
                x = (point.x * self.cell_size) + self.cell_size // 2
                y = (point.y * self.cell_size) + self.cell_size // 2
                points.append((x, y))

            intersect = False
            # check fov intersection
            for wall in self.walls:
                intersect = wall.rect.clipline(points[0], points[-1])

            if intersect:
                pygame.draw.line(self.screen, 'green', points[0], points[-1])
            else:
                pygame.draw.line(self.screen, 'blue', points[0], points[-1])

    # call on rays pulse
    def find_path(self, player_pos):
        # start
        start_x, start_y = self.rect.centerx // self.cell_size, self.rect.centery // self.cell_size
        start = self.grid.node(start_x, start_y)

        # end
        end_x, end_y = player_pos[0] // self.cell_size, player_pos[1] // self.cell_size
        end = self.grid.node(end_x, end_y)

        h = self.calculate_h_value((start_x, start_y), (end_x, end_y))
        if h <= self.fov_radius:
            # path
            finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
            self.path = finder.find_path(start, end, self.grid)[0]

            self.grid.cleanup()
            self.create_path_points_rects()
            self.get_direction()

    def draw_path(self, screen):
        if self.path:
            points = []
            for point in self.path:
                x = (point.x * self.cell_size) + self.cell_size // 2
                y = (point.y * self.cell_size) + self.cell_size // 2
                points.append((x, y))

            pygame.draw.lines(screen, 'red', False, points, 5)

        self.intersect_walls()

    def create_path_points_rects(self):
        if self.path:
            self.path_points = []
            for point in self.path:
                x = (point.x * self.cell_size) + self.cell_size // 2
                y = (point.y * self.cell_size) + self.cell_size // 2
                rect = pygame.Rect((x - 2, y - 2), (4, 4))
                self.path_points.append(rect)

    def get_direction(self):
        if len(self.path_points) > 1:
            start = pygame.math.Vector2(self.pos)

            # using [1] not [0] to avoid inconsistent random direction bug
            end = pygame.math.Vector2(self.path_points[1].center)

            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    def path_point_reached(self):
        if self.path_points:
            for rect in self.path_points:
                if rect.collidepoint(self.pos):
                    del self.path_points[0]
                    self.get_direction()
        else:
            self.empty_path()

    def update(self, player: Player):
        self.pos += self.direction * self.speed
        self.path_point_reached()
        self.rect.center = self.pos

        self.find_path((player.rect.x, player.rect.y))
