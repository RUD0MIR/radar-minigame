import math


class Line:
    def __init__(self, p0, p1):
        self.p0 = p0
        self.p1 = p1
        self.d = self.get_distance(p0, p1)

    def get_point(self, distance_from_p0):
        if self.d == 0:
            return self.p0

        p0 = self.p0
        p1 = self.p1
        dt = distance_from_p0

        t = dt / self.d
        p2 = ((1 - t) * p0[0] + t * p1[0]), ((1 - t) * p0[1] + t * p1[1])
        return p2

    @staticmethod
    def get_distance(p0, p1):
        return math.sqrt((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2)

    def is_point_on_line(self, p):
        dt = self.get_distance(self.p0, p)
        t = dt / self.d
        print(t)
        return 0 < t < 1

    def x_vector_direction(self):
        return self.p0[0] - self.p1[1]

    def y_vector_direction(self):
        return self.p0[1] - self.p1[1]
