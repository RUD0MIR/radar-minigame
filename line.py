import math

from shapely import Point


class Line:
    def __init__(self, p0, p1):
        self.p0 = Point(p0)
        self.p1 = Point(p1)
        self.d = self.get_distance(p0, p1)

    def get_point(self, distance_from_p0):
        p0 = self.p0
        p1 = self.p1
        dt = distance_from_p0

        t = dt / self.d
        p2 = ((1 - t) * p0.x + t * p1.x), ((1 - t) * p0.y + t * p1.y)
        return p2

    @staticmethod
    def get_distance(p0, p1):
        return math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)

    def is_on_line(self, p):
        dt = self.get_distance(self.p0, p)
        t = dt / self.d
        return 0 < t < 1
