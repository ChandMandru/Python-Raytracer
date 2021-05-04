from PIL import Image
from Camera import Camera
from Sphere import Sphere
from Triangle import Triangle
from Plane import Plane
import numpy as np


IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200
BACKGROUND_COLOR = (255,255,255) #Keine Hintergrund Farbe also Schwarz

#NEEDED FOV ,ASPECT RATIO, Auflösung des Bildes,e,c,up

eyeCenter = np.array([0,1.8,10])
sichtpunkt = np.array([0,3,0])
up = np.array([0,1,0])
sichtwinkel = 45  #Also 90 FOV

test_camera = Camera(eyeCenter,sichtpunkt,up,sichtwinkel)
image = Image.new('RGB',(IMAGE_WIDTH,IMAGE_HEIGHT))



objectlist = [
Sphere(np.array([0,1.5,-10]),2,(255,0,0)),
Sphere(np.array([-2.5,6,-10]),2,(0,255,0)),
Sphere(np.array([2.5,6,-10]),2,(0,0,255)),
Triangle(np.array([0,1.5,-10]),np.array([-2.5,6,-10]),np.array([2.5,6,-10]),(0,255,255)),
Plane(np.array([0,8,-10]),np.array([0,-1,0]),(255,255,0))
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
                        color = object.colorAt(ray) #Farbe des Treffpunkts lesen

            if x == IMAGE_WIDTH/2 or y == IMAGE_HEIGHT/2:
                image.putpixel((x,y),(0,0,0))
            else:
                image.putpixel((x,y), color) #beim Image diese Farbe and die Pixel Koordinaten setzen


test_camera.initCameraView(IMAGE_WIDTH,IMAGE_HEIGHT)

rayTracing(test_camera)

image.save("Test.png")
image.show()
