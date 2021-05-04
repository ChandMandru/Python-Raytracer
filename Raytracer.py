from PIL import Image
from Camera import Camera
from Sphere import Sphere
from Triangle import Triangle
from Plane import Plane
from Light import Light
from Checkerboard import CheckerboardMaterial
import numpy as np


IMAGE_WIDTH = 400
IMAGE_HEIGHT = 400
BACKGROUND_COLOR = (255,255,255) #Keine Hintergrund Farbe also Schwarz

#NEEDED FOV ,ASPECT RATIO, Auflösung des Bildes,e,c,up



eyeCenter = np.array([0,1.8,10])
sichtpunkt = np.array([0,3,0])
up = np.array([0,1,0])
sichtwinkel = 45  #Also 90 FOV

test_camera = Camera(eyeCenter,sichtpunkt,up,sichtwinkel)
Checkerboard = CheckerboardMaterial(0,0,0)
Light = Light(np.array([30,30,10]),(255,255,255))

image = Image.new('RGB',(IMAGE_WIDTH,IMAGE_HEIGHT))



objectlist = [
Sphere(np.array([0,1.5,-10]),2,(255,0,0)),
Sphere(np.array([-2.5,6,-10]),2,(0,255,0)),
Sphere(np.array([2.5,6,-10]),2,(0,0,255)),
Triangle(np.array([0,1.5,-10]),np.array([-2.5,6,-10]),np.array([2.5,6,-10]),(0,255,255)),
Plane(np.array([0,8,-10]),np.array([0,-1,0]),Checkerboard)
]

objectlist1 = [
Sphere(np.array([0,3,-1]),0.5,(255,0,0)),
Sphere(np.array([0,3,-5]),0.5,(0,255,0)),
Sphere(np.array([0,3,-10]),0.5,(0,0,255))
]


def calcGS(val):
    return (int(val*4),int(val*4),int(val*4))

def rayTracing(camera):
    for x in range(IMAGE_WIDTH):
        for y in range(IMAGE_HEIGHT): #Durch alle Bild Pixel durchlaufen 
            ray = camera.calcRayFromCam(x,y) #Für jeden Pixel ein Ray erstellen mit den Jeweiligen pixeln als koordinate
            maxdist = float('inf')
            color = BACKGROUND_COLOR  #Hintergrund Farbe festlegen
            for object in objectlist :  
                hitdist = object.intersectionParameter(ray) #Ray Distanz zu getroffenem Objekt
                if hitdist :
                    if hitdist < maxdist:
                        maxdist = hitdist #Auf Kleinste Distanz setzen
                        if isinstance(object,Plane):
                            color = object.colorAt(ray,maxdist) #Farbe des Treffpunkts lesen
                        else:
                            color = object.colorAt(ray)

            if x == IMAGE_WIDTH/2 or y == IMAGE_HEIGHT/2:
                image.putpixel((x,y),(0,0,0))
            else:
                image.putpixel((x,y), color) #beim Image diese Farbe and die Pixel Koordinaten setzen

#Hauptschleife der Klasse
def rayTracing2(camera):
    for x in range(IMAGE_WIDTH):
        for y in range(IMAGE_HEIGHT):
            ray = camera.calcRayFromCam(x,y)
            color = traceRay(0,ray)
            image.putpixel((x,y),color)


def traceRay(level,ray):
    hitPointData = intersect(level , ray , maxlevel)
    if hitPointData:
        if level <= maxlevel:
            return shade(level , hitPointData)
    return BACKGROUND_COLOR

def shade(hitpPointData):   
    directColor = computeDirectLight(hitpPointData)

    reflectedRay = computeReflectedRay(hitpPointData)
    reflectColor = traceRay(level+1,reflectedRay)

    return directColor + reflectColor #CHECK VL IF STUCK SKRIPT

def intersect(level,ray,maxlevel):
    hitObjekt  = None
    maxdistance = float('inf')

    for object in objectlist:
        hitdist  = object.intersectionParameter(ray)

        if hitdist:
            if hitdist < maxdistance and hitdist > 0:
                maxdistance = hitdist
                #Erstellt ein Objekt aus dem Aktuellen Objekt und dem Punkt wo sich der Strahl (am kürzesten) mit dem Objekt schneidet, der distanz dazu, und dem Strahl objekt selbst
                hitObjekt =(object,ray.pointAtParameter(maxdistance),maxdistance,ray)
            return hitObjekt



test_camera.initCameraView(IMAGE_WIDTH,IMAGE_HEIGHT)

rayTracing(test_camera)

image.save("Test.png")
image.show()
