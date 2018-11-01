class Constelacio:
    def __init__(self, nom, url):
        self.nom = nom
        self.url = url
        # self.__getData()


    def printConstelacioEnPantalla(self):
        print("nom : {}".format(self.nom))
        print("url : {}".format(self.url))
