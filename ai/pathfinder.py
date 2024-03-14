import random

import pygame
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Pathfinder:
    def __init__(self, cell_size, matrix, fov_radius, path_modifier: float):
        self.cell_size = cell_size
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)

        self.path = []
        self.path_points = []
        self.path_modifier = path_modifier

        self.fov_radius = fov_radius
        self.direction = pygame.math.Vector2(0, 0)

    def randomized_manhattan(self, dx, dy) -> float:
        return dx + dy + self.path_modifier

    @staticmethod
    def calculate_h_value(start, end):
        return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5

    def create_path_points_rects(self):
        if self.path:
            self.path_points = []
            for point in self.path:
                x = (point.x * self.cell_size) + self.cell_size // 2
                y = (point.y * self.cell_size) + self.cell_size // 2
                rect = pygame.Rect((x - 2, y - 2), (4, 4))
                self.path_points.append(rect)

    def get_direction(self, pos):
        if len(self.path_points) > 1:
            start = pygame.math.Vector2(pos)

            # using [1] not [0] to avoid inconsistent random direction bug
            end = pygame.math.Vector2(self.path_points[1].center)

            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.path = []

    def find_path(self, start_pos, end_pos):
        # start
        start_x, start_y = start_pos[0] // self.cell_size, start_pos[1] // self.cell_size
        start = self.grid.node(start_x, start_y)

        # end
        end_x, end_y = end_pos[0] // self.cell_size, end_pos[1] // self.cell_size
        end = self.grid.node(end_x, end_y)

        h = self.calculate_h_value((start_x, start_y), (end_x, end_y))
        if h <= self.fov_radius:
            # path
            finder = AStarFinder(
                heuristic=self.randomized_manhattan,
                diagonal_movement=DiagonalMovement.always
            )

            self.path = finder.find_path(start, end, self.grid)[0]
            self.grid.cleanup()
            self.create_path_points_rects()

    def check_path_points_collision(self, pos):
        if self.path_points:
            for rect in self.path_points:
                if rect.collidepoint(pos):
                    del self.path_points[0]
                    self.get_direction(pos)
        else:
            self.path = []

    def draw_path(self, screen):
        if self.path:
            points = []
            for point in self.path:
                x = (point.x * self.cell_size) + self.cell_size // 2
                y = (point.y * self.cell_size) + self.cell_size // 2
                points.append((x, y))

            pygame.draw.lines(screen, (0, 0, 255), False, points, 2)
