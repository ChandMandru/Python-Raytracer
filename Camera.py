import numpy as np
from Ray import Ray


class Camera(object):
    """Klasse für das Kamera Objekt. Kartesiches Koordinaten System erstellen anhand von 3 Gegebenen Punkten"""

    def __init__(self,eyeCenter,sichtpunkt,up,sichtwinkel):
        self.eyeCenter = eyeCenter
        self.sichtpunkt = sichtpunkt
        self.up = up
        self.sichtwinkel = sichtwinkel

        # Normalisieren f = vektor von Center zu Objekt
        self.f = (sichtpunkt-eyeCenter)/(np.linalg.norm(sichtpunkt-eyeCenter))
        #Cross ist Kreuzprodukt und gibt vektor der auf beiden Vektoren senkrecht Steht(f,up) und norm gibt die Länge des vektors an wenn durch 
        self.s = np.cross(self.f,up) / (np.linalg.norm(np.cross(self.f,up)))
        #Kreuzprodukt von s und f für letzen Vektor
        self.u = np.cross(self.s,self.f)


    def initCameraView(self,imgWidth,imgHeight):
        self.aspectRatio = imgWidth / imgHeight #Bildverhältniss
        self.alpha = self.sichtwinkel/2 #FOV Angabe halbiert
        self.height = 2 * np.tan(self.alpha)# *2 ergibt volle höhe
        self.width = self.aspectRatio * self.height #Bildverhältniss * die höhe ergibt breite
        self.pixWidth = self.width / (imgWidth-1)   #Pro Pixel Höhe
        self.pixHeight = self.height / (imgHeight-1)#Pro Pixel Breite

    def calcRayFromCam(self,x,y):
        xcomp = self.s * (x * self.pixWidth - self.width/2)
        ycomp = self.u * (y * self.pixHeight - self.height/2) 
        return Ray(self.eyeCenter,self.f+xcomp+ycomp)