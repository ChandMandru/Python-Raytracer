import numpy as np
from PIL import Image
import time

from Camera import Camera
from Checkerboard import CheckerboardMaterial
from Light import Light
from Plane import Plane
from Sphere import Sphere
from Triangle import Triangle
from Ray import Ray

IMAGE_WIDTH = 200
IMAGE_HEIGHT = 200
BACKGROUND_COLOR = (0,0,0) #Keine Hintergrund Farbe also Schwarz

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
Triangle(np.array([0,1.5,-10]),np.array([-2.5,6,-10]),np.array([2.5,6,-10]),(0,0,0)),
Plane(np.array([0,8,-10]),np.array([0,-1,0]),Checkerboard)
]

objectlist1 = [
Triangle(np.array([0,1.5,-10]),np.array([-2.5,6,-10]),np.array([2.5,6,-10]),(0,0,0))
]

shadowAmbiet = 0.1
noShadowAmbiet = 0.5
diffusion = 0.5
specular = 0.5
exp_shiny = 10
reflection = 0.2


maxlevel = 3


def normalized(vek):
    norm = np.linalg.norm(vek)

    if norm == 0:
        return vek

    return vek / norm    

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
            color_values = traceRay(0,ray)
            color = (int(color_values[0]),int(color_values[1]),int(color_values[2]))
            image.putpixel((x,y),color)

def intersect(level,ray,maxlevel):
    hitObjekt  = None #Daten Des Getroffenen Objektes
    maxdistance = float('inf')

    for object in objectlist:
        hitdist  = object.intersectionParameter(ray) #Berechne für Jedes Objekt die Schnittpunkte mit dem Mitgegebenem Ray

        if hitdist:
            if hitdist < maxdistance and hitdist > 0:
                maxdistance = hitdist
                #Erstellt ein Objekt aus dem Aktuellen Objekt und dem Punkt wo sich der Strahl (am kürzesten) mit dem Objekt schneidet, der distanz dazu, und dem Strahl objekt selbst
                hitObjekt =(object,ray.pointAtParameter(maxdistance),maxdistance,ray)
            return hitObjekt

def traceRay(level,ray):
    hitObjekt = intersect(level , ray , maxlevel)
    if hitObjekt:
        if level <= maxlevel:
            return shade(level ,hitObjekt)
    return BACKGROUND_COLOR


def shade(level,hitObjekt):   
    directColor = computeDirectLight(hitObjekt)
    reflectedRay = computeReflectedRay(hitObjekt)
    reflectColor = traceRay(level+1,reflectedRay)

    return directColor + reflection * np.array(reflectColor) #CHECK VL IF STUCK SKRIPT

def computeDirectLight(hitObjekt):
    currObj = hitObjekt[0] #Aktuelles mit zu arbeitendem Objekt aus der welt
    currRay = hitObjekt[3]
    currMaxdist = hitObjekt[2]

    if currObj is not None :    #Wenn es ein Objekt gibt
        schnittpunkt = hitObjekt[1] #Punkt an dem der Ray das Objekt Schneidet
        towards_light_vek = Ray(schnittpunkt,normalized(Light.pos - schnittpunkt)) #Berechnet sich durch der Position des Lichtes und der Position des Schnittpunkts des Rays mit dem Objekt in der Welt

        shadow = isInShadow(currObj,towards_light_vek) #Prüft ob der schnittpunkt im Schatten ist

        if shadow == True:
            #Prüfen ob es sich um eine Plane Handelt da diese eine andere Farbanwendung haben
            if isinstance(currObj,Plane):
                color = np.array(currObj.colorAt(currRay,currMaxdist))
            else:
                color = shaderPhong(schnittpunkt,hitObjekt,shadowAmbiet)
        else:
            color = shaderPhong(schnittpunkt,hitObjekt,noShadowAmbiet)
    return color

#Prüft ob Zwischen einem Gegebenen Objekt und dem Licht Objekt min. Noch ein Objekt liegt also "Ob es im Schatten" von einem Anderem Objekt Liegt
def isInShadow(currObj,towards_light_vek):
    for o in objectlist:
        if currObj is not None:
            if o is not currObj:    #Das element selbst, soll nicht gecheckt werden
                intersectCheck = o.intersectionParameter(towards_light_vek) #Hier wird geschaut ob der Strahl richtung licht Noch ein objekt schneidet oder nicht, also ob ein Objekt zwischen dem licht und unserem ausgangs objekt liegt

                if intersectCheck is not None and intersectCheck > 0:
                    return True
    return False            

def computeReflectedRay(hitObjekt):
    currObj = hitObjekt[0]
    currSchnitt = hitObjekt[1]
    currRay = hitObjekt[3]

    normVek = normalized(currObj.normalAt(currSchnitt))
    reflect = normalized(currRay.direction - 2* np.dot(currRay.direction,normVek)*normVek)
    refRay = Ray (currSchnitt,reflect)

    return refRay

def shaderPhong(schnittpunkt,hitObjekt,ambiet):

    currObj = hitObjekt[0]
    currRay = hitObjekt[3]
    currMaxdist = hitObjekt[2]

    if isinstance(currObj,Plane):#Falls es eine Ebene ist muss wieder die spezifische färbungs methode angewendet werden
        currColor = np.array(currObj.colorAt(currRay,currMaxdist))
    else:
        currColor = np.array(currObj.color_in_RGB)

    npLight = np.array(Light.color_in_RGB)

    toLightVek = normalized(Light.pos - schnittpunkt)
    normVek = normalized(currObj.normalAt(schnittpunkt))
    reflect = toLightVek - (2* abs(np.dot(normVek,toLightVek))*normVek) #Reflektion vom Einfallswinkel ergibt richtung vom Ausfallswinkel
    n = normalized(schnittpunkt - test_camera.eyeCenter)

    finalCol = currColor * ambiet + npLight * diffusion * np.dot(toLightVek,normVek) + npLight * specular * (np.dot(reflect,-n)**exp_shiny)
    return finalCol

test_camera.initCameraView(IMAGE_WIDTH,IMAGE_HEIGHT)

start = time.perf_counter()
rayTracing2(test_camera)
end = time.perf_counter()

print("Time Rendering :",end-start)

image.save("Test.png")
image.show()

