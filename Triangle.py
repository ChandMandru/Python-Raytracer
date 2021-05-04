import numpy as np

class Triangle(object):
    def __init__(self, a, b, c,color_in_RGB):
        self.a=a # point
        self.b=b # point
        self.c=c # point
        self.u = self.b - self.a # direction vector
        self.v = self.c - self.a # direction vector
        self.color_in_RGB = color_in_RGB

    def __repr__(self):
        return 'Triangle(%s,%s,%s)' %(repr(self.a), repr(self.b),repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = np.cross(ray.direction,self.v)
        dvu = np.dot(dv,self.u)


        if dvu == 0.0:
            return None
        wu = np.cross(w,self.u)    
        r = (np.dot(dv,w)) / dvu
        s = (np.dot(wu,ray.direction)) / dvu

        if 0<=r and r<=1 and 0<=s and s<=1 and r+s<=1:
            return (np.dot(wu,self.v)) / dvu
        else :
            return None

    def normalAt(self, p):
        return np.linalg.norm(np.cross(self.u,self.v))

    def colorAt(self, ray):
        return self.color_in_RGB    

def normalized(vek):
    norm = np.linalg.norm(vek)

    if norm == 0:
        return vek

    return vek / norm