import math

import pygame

from map import Line


class Ray:
    def __init__(self, mouse_pos, angle):
        self.x = mouse_pos[0]
        self.y = mouse_pos[1]
        self.dir = (math.cos(angle), math.sin(angle))

    def update(self, mouse_pos):
        self.x = mouse_pos[0]
        self.y = mouse_pos[1]

    def checkCollision(self, line: Line):
        x1 = line.start_pos[0]
        y1 = line.start_pos[1]
        x2 = line.end_pos[0]
        y2 = line.end_pos[1]

        x3 = self.x
        y3 = self.y
        x4 = self.x + self.dir[0]
        y4 = self.y + self.dir[1]

        # Using line-line intersection formula to get intersection point of ray and line
        # Where (x1, y1), (x2, y2) are the ray pos and (x3, y3), (x4, y4) are the line pos
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)

        if denominator == 0:
            return None

        t = numerator / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 1 > t > 0 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            collidePos = [x, y]
            return collidePos


# TODO get data from tmx, by points, and pass it to this class


class Rays:
    def __init__(self, lines: list[Line], surface):
        self.surface = surface
        self.lines = lines
        self.mouse_pos = pygame.mouse.get_pos()
        self.rays = []
        self.rays_color = (0, 0, 0, 0)
        self.rays_count = 360

        self.closest_multiplier = 0
        self.max_closest_multiplier = 200
        self.closest_increase = 2

        self.lastClosestPoint = (0, 0)

        self.generate_rays()

    def generate_rays(self):
        for i in range(0, 360, int(360 / self.rays_count)):
            self.rays.append(Ray(self.mouse_pos, math.radians(i)))

    def draw_rays(self):  # (0, 0, 0, 0)
        for ray in self.rays:
            closest = 10 * self.closest_multiplier
            closest_point = None
            for line in self.lines:
                intersect_point = ray.checkCollision(line)
                if intersect_point is not None:
                    # Get distance between ray source and intersect point
                    ray_dx = ray.x - intersect_point[0]
                    ray_dy = ray.y - intersect_point[1]

                    # If the intersect point is closer than the previous closest intersect point, it becomes the
                    # closest intersect point
                    distance = math.sqrt(ray_dx ** 2 + ray_dy ** 2)
                    if distance < closest:  # self.rays_length
                        # self.rays_length = distance
                        closest = distance
                        closest_point = intersect_point

            if closest_point is not None:
                pygame.draw.rect(self.surface, 'Red', (closest_point, (5, 5)))
                # pygame.draw.line(self.surface, self.rays_color, (ray.x, ray.y), closest_point)


    def rays_pulse(self):
        if self.closest_multiplier == self.max_closest_multiplier:
            self.closest_multiplier = 0
        else:
            self.closest_multiplier += self.closest_increase

    def update(self, mouse_pos):
        self.rays_pulse()

        if self.closest_multiplier == 0:
            for ray in self.rays:
                ray.update(mouse_pos)
