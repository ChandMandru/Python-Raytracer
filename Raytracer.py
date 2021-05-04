from PIL import Image
from Camera import Camera
import numpy as np

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200
BACKGROUND_COLOR = (0,0,0) #Keine Hintergrund Farbe also Schwarz

#NEEDED FOV ,ASPECT RATIO, Auflösung des Bildes,e,c,up

eyeCenter = np.array([0,1.8,10])
sichtpunkt = np.array([0,3,0])
up = np.array([0,1,0])
sichtwinkel = 45  #Also 90 FOV

test_camera = Camera(eyeCenter,sichtpunkt,up,sichtwinkel)
image = Image.new('RGB',(IMAGE_WIDTH,IMAGE_HEIGHT))

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
            image.putpixel((x,y), color) #beim Image diese Farbe and die Pixel Koordinaten setzen



image.show()