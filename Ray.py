import numpy as np

class Ray(object):

    def __init__(self, origin, direction):
        self.origin = origin #Ausgangspunkt
        self.direction = normalize(direction) #vector Normierungs funktion einfügen linalg.norm

    def __repr__(self):
        return ’Ray(%s,%s)’ %(repr(self.origin), repr(self.direction))

    def pointAtParameter(self , t):
        return self.origin + self.direction * t #Skaliert die richtung mal t

#Normalisiert einen Vektor falls schon normalisiert wird eingabe vektor zurückgegeben
def normalize(vek):
    normalized = np.linalg.norm(vek)

    if normalized == 0:
        return vek

    return vek/normalized