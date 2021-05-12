import numpy as np
from PIL import Image
import time

from Camera import Camera
from Light import Light
from Ray import Ray
from Material import Material
from WorldObjects import *
import tqdm
import threading
import multiprocessing

""" VON - Changeable Parameters für Bildeinstellungen"""
IMAGE_WIDTH =100
IMAGE_HEIGHT =100
BACKGROUND_COLOR = (0,0,0) #Keine Hintergrund Farbe also Schwarz

sichtwinkel = 45  #Also 90 FOV
exp_shiny = 10  
reflection = 0.2 #Reflektionsstärke
maxlevel = 1    #Bounces an reflektionen

Light = Light(np.array([20,-20,10]),(255,255,255))  #Lichtposition und Farbe

SphereMaterial = Material(0.1,0.5,0.5,0.5)          #Materialien
TriangleMaterial = Material(0.1,0.5,0.5,0.5)
PlaneMaterial = Material(0.1,0.5,0.5,0.5)

normalCam = Camera(np.array([0,1.8,10]),np.array([0,3,0]),np.array([0,1,0]),sichtwinkel)
normalCam.initCameraView(IMAGE_WIDTH,IMAGE_HEIGHT)
""" BIS - Changeable Parameters für Bildeinstellungen"""



Checkerboard = CheckerboardMaterial(0,0,0)
image = Image.new('RGB',(IMAGE_WIDTH,IMAGE_HEIGHT))

'''Objekte die in der welt eingefügt werden liegen in objectlist falls Custom Hier bitte Objekte Einfügen / Rausnehmen'''
objectlist = [
Sphere(np.array([0,1.5,-10]),2,(255,0,0),SphereMaterial),
Sphere(np.array([-2.5,6,-10]),2,(0,255,0),SphereMaterial),
Sphere(np.array([2.5,6,-10]),2,(0,0,255),SphereMaterial),
Triangle(np.array([0,1.5,-10]),np.array([-2.5,6,-10]),np.array([2.5,6,-10]),(255,255,0),TriangleMaterial),
Plane(np.array([0,10,0]),np.array([0,-10,-3.5]),Checkerboard,PlaneMaterial)
]

#Hauptmethode zum Ausführen verschiedener Funktionen
def renderStart():   

    start = time.perf_counter()

    rayTracing2(normalCam)                     # Normal Render
    #Thread_Processing(squirrelRender,None)     # Squirrel Threading
    #processing_Method(squirrelRender,None)     # Squirrel Processing
    #Thread_Processing(rayTracing2,normalCam)   # Normal Threading
    #processing_Method(rayTracing2,normalCam)   # Normal Processing
    #squirrelRender()                           # Normal Squirrel Render


    end = time.perf_counter()

    print("Time Rendering :",end-start)

    image.save("Result.png")
    image.show()







#Normalisiert einen Vektor
def normalized(vek):
    norm = np.linalg.norm(vek)

    if norm == 0:
        return vek

    return vek / norm    

def squirrelRender():
    global objectlist

    sqlist = []
    squirr = open('squirrel.obj','r')
    txt = squirr.readlines()
    vecs = [list(map(float,x.rstrip().split(" ")[1:])) for x in txt if x.startswith("v")]
    corners = [list(map(int,x.rstrip().split(" ")[1:])) for x in txt if x.startswith("f")]

    for n in range(len(corners)):
        triangle = Triangle(np.array(vecs[corners[n][0]-1]),np.array(vecs[corners[n][1]-1]),np.array(vecs[corners[n][2]-1]),(255,0,0),TriangleMaterial)
        sqlist.append(triangle)

    objectlist = sqlist 
    tempCam = Camera(np.array([0,1.8,-6]),np.array([0,2,0]),np.array([0,-1,0]),sichtwinkel)  
    tempCam.initCameraView(IMAGE_WIDTH,IMAGE_HEIGHT)
    rayTracing2(tempCam)

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
    for x in tqdm.tqdm(range(IMAGE_WIDTH)):
        for y in range(IMAGE_HEIGHT):
            ray = camera.calcRayFromCam(x,y)
            color_values = traceRay(0,ray)
            color = (int(color_values[0]),int(color_values[1]),int(color_values[2]))
            image.putpixel((x,y),color)

#Ray folgen wenn es etwas Trifft farbe berechnen per Shade wenn nicht dann Hintergrundfarbe setzen
def traceRay(level,ray):
    hitObjekt = intersect(level , ray , maxlevel)
    if hitObjekt:
        if level <= maxlevel:
            return shade(level ,hitObjekt)
    return BACKGROUND_COLOR


#Gibt für einen Ray ein HitObjekt zurück Welches 1. Das Schnittobjekt 2.Den Schnittpunkt mit dem Objekt 3.Die länge vom ausgangsray bis zum objekt 4. den Ray, an
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

#Shade also Farbberechnung , Erst Direkte Farbe per Compute direkt light und dann Reflected ray berechnen Falls es einen gibt, beide kriegen das hitobjekt mit
def shade(level,hitObjekt):   
    directColor = computeDirectLight(hitObjekt)
    reflectedRay = computeReflectedRay(hitObjekt)
    reflectColor = traceRay(level+1,reflectedRay)

    return directColor + reflection * np.array(reflectColor)

#Berechtnet die Farbe am Aktuellen Schnittpunkt
def computeDirectLight(hitObjekt):
    currObj = hitObjekt[0] #Aktuelles mit zu arbeitendem Objekt aus der welt
    currRay = hitObjekt[3]
    currMaxdist = hitObjekt[2]
    color = (0,0,0)

    if currObj is not None and hitObjekt[0]:    #Wenn es ein Objekt gibt


        schnittpunkt = hitObjekt[1] #Punkt an dem der Ray das Objekt Schneidet
        towards_light_vek = Ray(schnittpunkt,Light.pos - schnittpunkt) #Berechnet sich durch der Position des Lichtes und der Position des Schnittpunkts des Rays mit dem Objekt in der Welt
        shadow = isInShadow(currObj,towards_light_vek) #Prüft ob der schnittpunkt im Schatten ist

        if shadow == True:
            #Prüfen ob es sich um eine Plane Handelt da diese eine andere Farbanwendung haben
            if isinstance(currObj,Plane):
                color = np.array(currObj.colorAt(currRay,currMaxdist)) * currObj.getMaterial().getShadowAmbient()
            else:
                color = shaderPhong(schnittpunkt,hitObjekt,currObj.getMaterial().getShadowAmbient())
        else:
            #Falls es nicht im schatten ist mit Phong Shading berechnen
            color = shaderPhong(schnittpunkt,hitObjekt,currObj.getMaterial().getNoShadowAmbient())

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

#Berechnet den Reflektionsstrahl von einem Hitobjekt und seinem Schnittpunkt
def computeReflectedRay(hitObjekt):
    currObj = hitObjekt[0]
    currSchnitt = hitObjekt[1]
    currRay = hitObjekt[3]

    normVek = normalized(currObj.normalAt(currSchnitt))
    reflect = normalized(currRay.direction - 2 * np.dot(currRay.direction,normVek)*normVek)
    refRay = Ray (currSchnitt,reflect)

    return refRay


def shaderPhong(schnittpunkt,hitObjekt,ambient):

    currObj = hitObjekt[0]
    currMaxdist = hitObjekt[2]
    currRay = hitObjekt[3]

    #Falls es eine Ebene ist muss wieder die spezifische färbungs methode angewendet werden
    if isinstance(currObj,Plane):
        currColor = np.array(currObj.colorAt(currRay,currMaxdist))
    else:
        currColor = np.array(currObj.colorAt())

    npLight = np.array(Light.color_in_RGB) #Umrechnung der Lichtfarbe in ein npArray damit man damit Rechnen Kann
    toLightVek = normalized(Light.pos - schnittpunkt)
    normVek = normalized(currObj.normalAt(schnittpunkt))
    n = normalized(schnittpunkt - normalCam.eyeCenter)
    reflect = toLightVek - (2 * abs(np.dot(normVek,toLightVek))*normVek) #Reflektion vom Einfallswinkel ergibt richtung vom Ausfallswinkel

    return currColor * ambient + (npLight * currObj.getMaterial().getDiffuse() * np.dot(toLightVek,normVek)) #+ (npLight * currObj.getMaterial().getSpecular() *(np.dot(reflect,-n)**exp_shiny)) #Macht Dreieck lighting buggy


def Thread_Processing(method,args):
    Threads=[]

    #4 Threads
    for n in range(4):
        if args:
            t = threading.Thread(target = method,args=(args,))
            Threads.append(t)
            print(f"Thread {n} startet")
            t.start()
        else:
            t = threading.Thread(target = method)
            Threads.append(t)
            print(f"Thread {n} startet")
            t.start()

    for k in range(4):
        Threads[k].join()
        print(f"Thread {k} endet")    

def processing_Method(method,args):

    Threads=[]

    for n in range(4):
        if args:
            t = multiprocessing.Process(target = method,args=(args,))
            Threads.append(t)
            print(f"Thread {n} startet")
            t.start()
        else:
            t = multiprocessing.Process(target = method)
            Threads.append(t)
            print(f"Thread {n} startet")
            t.start()

    for k in range(4):
        Threads[k].join()

if __name__ == '__main__':
    renderStart()