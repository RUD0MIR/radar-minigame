import math

import pygame

from ai.map import Walls


class LineFov:
    def __init__(self, fov_radius):
        self.radius = fov_radius
        self.start_pos = None
        self.end_pos = None

    def fov_line_blocked_by_wall(self, start_pos, end_pos, walls: Walls):
        self.start_pos = start_pos
        self.end_pos = end_pos
        line = (start_pos, end_pos)
        return any(wall.rect.clipline(line) for wall in walls)

    def draw_fov_line(self, screen, walls):
        fov_line = (self.start_pos, self.end_pos)
        color = "red" if any(wall.rect.clipline(fov_line) for wall in walls) else "green"
        pygame.draw.line(screen, color, fov_line[0], fov_line[1])

    def radius_exceeded(self, start_pos, end_pos,):
        # sqrt{(x_2 - x_1) ^ 2 + (y_2 - y_1) ^ 2}
        line_length = math.sqrt((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2)
        return line_length > self.radius

