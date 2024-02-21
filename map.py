import math

import pygame
from pytmx.pytmx import Point
from shapely import geometry, ops


class Line:
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.slope_x = end_pos[0] - start_pos[0]
        self.slope_y = end_pos[1] - start_pos[1]
        if self.slope_x == 0:
            self.slope = 0
        else:
            self.slope = self.slope_y / self.slope_x
        self.length = math.sqrt(self.slope_x ** 2 + self.slope_y ** 2)


class Map:
    def __init__(self, tmx_data, surface):
        # self.lines_color = (0, 0, 0, 0)
        self.lines_color = 'white'
        self.surface = surface
        self.tmx_data = tmx_data
        self.lines = []

        self.get_lines_from_tmx()

    def get_lines_from_tmx(self):
        for obj in self.tmx_data.objects:

            points = obj.as_points
            for i in range(0, len(points)):
                if i + 1 < len(points):
                    line = Line((points[i].x, points[i].y), (points[i + 1].x, points[i + 1].y))
                    self.lines.append(line)
                elif i + 1 == len(points):
                    line = Line((points[i].x, points[i].y), (points[0].x, points[0].y))
                    self.lines.append(line)

    def draw_lines(self):
        for line in self.lines:
            pygame.draw.line(self.surface, self.lines_color, line.start_pos, line.end_pos, width=3)
