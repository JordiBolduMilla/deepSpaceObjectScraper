# Classe que representa un objecte constel.lació

class Constelacio:

    # constructor
    def __init__(self, nom, url):
        self.nom = nom
        self.url = url
        # self.__getData()

    # mètode públic per imprimir el contingut d'un objecte constelació per pantalla
    def printConstelacioEnPantalla(self):
        print("nom : {}".format(self.nom))
        print("url : {}".format(self.url))
