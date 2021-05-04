from PIL import Image
from Camera import Camera

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200
BACKGROUND_COLOR = (0,0,0) #Keine Hintergrund Farbe also Transparent

#NEEDED FOV ,ASPECT RATIO, Auflösung des Bildes,e,c,up

eyeCenter = numpy.array([0,1.8,10])
sichtpunkt = numpy.array([0,3,0])
up = numpy.array([0,1,0])
sichtwinkel = 45  #Also 90 FOV

camera = Camera(eyeCenter,sichtpunkt,up,sichtwinkel)

def rayTracing(camera):
    for x in range(IMAGE_WIDTH):
        for y in range(IMAGE_HEIGHT): #Durch alle Bild Pixel durchlaufen

            ray = camera.calcRayFromCam(x,y) #Für jeden Pixel ein Ray erstellen mit den Jeweiligen pixeln als koordinate
            maxdist = float(’inf’)
            color = BACKGROUND_COLOR  #Hintergrund Farbe festlegen
            for object in objectlist :  
                hitdist = object.intersectionParameter(ray) #Ray Distanz zu getroffenem Objekt
                if hitdist :
                    if hitdist < maxdist:
                        maxdist = hitdist #Auf Kleinste Distanz setzen
                        color = object.colorAt(ray) #Farbe des Treffpunkts lesen
            image.putpixel((x,y), color) #beim Image diese Farbe and die Pixel Koordinaten setzen
