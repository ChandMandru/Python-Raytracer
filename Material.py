class Material(object):

    def __init__(self,shadowAmbient,noShadowAmbient,diffuse,specular):
        self.shadowAmbient = shadowAmbient
        self.noShadowAmbient = noShadowAmbient
        self.diffuse = diffuse
        self.specular = specular

    def getShadowAmbient(self):
        return self.shadowAmbient

    def getNoShadowAmbient(self):
        return self.noShadowAmbient    

    def getDiffuse(self):
        return self.diffuse    

    def getSpecular(self):
        return self.specular