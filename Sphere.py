import numpy as np


class Sphere(object):
    
    def __init__(self, center, radius, color_in_RGB):
        self.center = center  # point
        self.radius = radius  # scalar
        self.color_in_RGB = color_in_RGB  # RGB Farbe der Kugel

    def __repr__(self):
        return 'Sphere(%s,%s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin  # Vektor von Ray Origin zu Kugel Center
        v = np.dot(co, ray.direction)   
        discriminant = v*v - np.dot(co, co) + self.radius * self.radius
        if discriminant < 0:
            return None
        else:
            return v - np.sqrt(discriminant)

    def normalAt(self, p):
        return normalized((p - self.center))

    def colorAt(self, ray):
        return self.color_in_RGB


def normalized(vek):
    norm = np.linalg.norm(vek)

    if norm == 0:
        return vek

    return vek / norm
