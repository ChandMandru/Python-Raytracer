import numpy as np

class Plane(object):
    def __init__(self, point, normal,color_in_RGB):
        self.point = point # point
        self.normal = normalized(normal) # vector
        self.color_in_RGB = color_in_RGB

    def __repr__(self):
        return 'Plane(%s,%s)' %(repr(self.point), repr(self.normal))

    def intersectionParameter(self , ray):
        op = ray.origin - self.point
        a = np.dot(op,self.normal)
        b = np.dot(ray.direction,self.normal)

        if b<0:
            return -a/b
        else :
            return None

    def normalAt(self, p):
        return self.normal

    def colorAt(self, ray,maxdist): #Punkt Statt Color ?
        return self.color_in_RGB.baseColorAt(ray.pointAtParameter(maxdist))    
   

def normalized(vek):
    norm = np.linalg.norm(vek)

    if norm == 0:
        return vek

    return vek / norm        