# Classe que representa un objecte profund

class ObjecteProfund:

    # constructor
    def __init__(self, nom, dades_objecte_profund, constelacio):
        self.nom = nom.replace(" / ", "/").replace(";","/")
        self.__dades_objecte_profund = dades_objecte_profund
        self.nom_catalogacio_1 = ""
        self.nom_catalogacio_2 = ""
        self.constelacio = constelacio
        self.__getData()

    # métode privat necessari per poder iterar sobre una col.leccio (llista, ...) d'objectes profunds
    def __iter__(self):
        return iter([self.nom,self.nom_catalogacio_1, self.nom_catalogacio_2, self.magnitud, self.tipus, self.tamany, self.ascencio_rectal, self.declinacio, self.constelacio])

    # mètode privat per manipular les dades llegides i 'netejar-les'
    def __cleanTokens(self, value):
        tokens = ['Magnitud: ', 'Tipo: ', 'Tamaño: ', 'AR: ', 'Dec: ']

        tmp_value = value
        for token in tokens:
            tmp_value = tmp_value.replace(token, '')

        if tmp_value == '':
            tmp_value = "NA"

        return tmp_value

    # mètode privat per omplir les propietats d'un objecte profund
    def __getData(self):
        __tokens_nom_objecte_profund = self.nom.strip().replace(";","/").split("/")
        if (len(__tokens_nom_objecte_profund) == 1):
            self.nom_catalogacio_1 = __tokens_nom_objecte_profund[0]
            self.nom_catalogacio_2 = ""
        else:
            self.nom_catalogacio_1 = __tokens_nom_objecte_profund[0]
            self.nom_catalogacio_2 = __tokens_nom_objecte_profund[1]

        self.magnitud = self.__cleanTokens(self.__dades_objecte_profund[0])
        self.tipus = self.__cleanTokens(self.__dades_objecte_profund[1])
        self.tamany = self.__cleanTokens(self.__dades_objecte_profund[2])
        self.ascencio_rectal = self.__cleanTokens(self.__dades_objecte_profund[3])
        self.declinacio = self.__cleanTokens(self.__dades_objecte_profund[4])

    # mètode públic per imprimir el contingut d'un objecte profund per pantalla
    def printObjecteProfund(self):
        print("nom : {}".format(self.nom))
        print("codi catalogacio 1 : {}".format(self.nom_catalogacio_1))
        print("codi catalogacio 2 : {}".format(self.nom_catalogacio_2))
        print("magnitud : {}".format(self.magnitud))
        print("tipus : {}".format(self.tipus))
        print("tamany : {}".format(self.tamany))
        print("ascencio rectal (AR) : {}".format(self.ascencio_rectal))
        print("declinació : {}".format(self.declinacio))
        print("constelacio : {}".format(self.constelacio))

