import numpy as np

def normalized(vek):
    norm = np.linalg.norm(vek)

    if norm == 0:
        return vek

    return vek / norm


class Sphere(object):
    
    def __init__(self, center, radius, color_in_RGB,material):
        self.center = center  # point
        self.radius = radius  # scalar
        self.color_in_RGB = color_in_RGB  # RGB Farbe der Kugel
        self.material = material

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

    def colorAt(self):
        return self.color_in_RGB

    def getMaterial(self):
        return self.material    


class Triangle(object):
    def __init__(self, a, b, c,color_in_RGB,material):
        self.a=a # point
        self.b=b # point
        self.c=c # point
        self.u = self.b - self.a # direction vector
        self.v = self.c - self.a # direction vector
        self.color_in_RGB = color_in_RGB
        self.material = material

    def __repr__(self):
        return 'Triangle(%s,%s,%s)' %(repr(self.a), repr(self.b),repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = np.cross(ray.direction,self.v)
        dvu = np.dot(dv,self.u)
        


        if dvu == 0.0:
            return None
        wu = np.cross(w,self.u)    
        r = np.dot(dv,w) / dvu
        s = np.dot(wu,ray.direction) / dvu

        if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r+s <= 1:
            return (np.dot(wu,self.v)) / dvu
        else:
            return None

    def normalAt(self, p):
        return normalized(np.cross(self.u,self.v))

    def getMaterial(self):
        return self.material     

    def colorAt(self):
        return self.color_in_RGB   

class Plane(object):
    def __init__(self, point, normal,color_in_RGB,material):
        self.point = point # point
        self.normal = normalized(normal) # vector
        self.color_in_RGB = color_in_RGB
        self.material = material

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

    def getMaterial(self):
        return self.material

class CheckerboardMaterial(object):
    def __init__(self , a, b, c):
        self.baseColor = (255,255,255)
        self.otherColor = (0, 0, 0)
        self.ambientCoefficient = 0.5
        self.diffuseCoefficient = 0.5
        self.specularCoefficient = 0.2
        self.checkSize = 1

    def baseColorAt(self , p):
        v = p
        v = v * (1.0 / self.checkSize) # Skalierung
        x = v[0]
        y = v[1]
        z = v[2]
        if (int(abs(x) + 0.5) + int(abs(y) + 0.5) + int(abs(z)+ 0.5)) %2:
            return self.otherColor
        return self.baseColor                       