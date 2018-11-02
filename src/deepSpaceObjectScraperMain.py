# Paquets i funcions utilitzades

import time
import os
import requests
from Constelacio import Constelacio
from ObjecteProfund import ObjecteProfund
from bs4 import BeautifulSoup
from Utils import writeDataset, getRealUrlFromImage, serializeImageFromUrl, desar_imatge_constelacio



# Traça d'inici ...
print("Iniciant web scraping ...")

# Definició de variables 'globals'

url_site = "http://atlasdeastronomia.com/"
url_site_constelacions = url_site + "constelaciones"
path_dataset = os.getcwd() + "/dataset/"
path_imatges = os.getcwd() + "/img/"
header_dataset= ['nom_complert_objecte','codi_catalogacio_1','codi_catalogacio_2','magnitud',
                 'tipus_objecte','tamany','ascensio_rectal','declinacio','constelacio']


# Obtenim la pàgina ppal on trobem el llistat de totes les constel.lacions
pagina_ppal = requests.get(url_site_constelacions)

llista_constelacions = []
llista_objectes_espai_profund = []

# "Parsegem" el contingut de la pàgina ppal ...
soup = BeautifulSoup(pagina_ppal.text, 'html.parser')
# ... i localitzem els nodes HTML que contenen les diferents constel.lacions ...
article_boxes_constelacions = soup.findAll("div", {"class" : "articlebox"})

# Iterem pels diferents nodes que representen cada constel.lació ...
for article_box_constelacio in article_boxes_constelacions:

    node_base = article_box_constelacio.article
    # ... i n'obtenim, el nom ...
    nom = node_base.find_next('div', {"class": "articledescrip"}).getText()
    # ... i la url de la pàgina on hi ha el detall dels diferents objectes profunds que la conformen
    # i la seva imatge ...
    url = url_site + node_base.header.h2.a['href']

    # Creem un objecte Constel.lació per desar la info ...
    constelacio_en_curs = Constelacio(nom, url)
    # ... i el desem en una llista per la seva posterior iteració ...
    llista_constelacions.append(constelacio_en_curs)
    # Traça per pantalla de l'objecte Constel.lació en curs 
    constelacio_en_curs.printConstelacioEnPantalla()

    # En aquest bloc, accedirem a la pàgina 'detall' de la Constel.lació en curs per
    # obtenir la seva imatge i les dades dels seus objectes profunds (aquests darrers conformaran el
    # nostre Dataset

    # Per evitar sobrecàrrega de peticions al servidor, entre accés i accés a cada una de les pàgina de detall
    # de cada Constel.lació deixarem passar un temps (10 vegades el temps que s'hagi trigat en fer la petició)

    # Per això, abans de la fer la petició, hem de posar un comptador 't0' que després ens permeti calcular
    # el temps que hem trigat ...
    t0 = time.time()

    # Accedim a la pàgina detall de la Constel.lació en curs ...
    pagina_constelacio_en_curs = requests.get(url)

    # Si tot ha anat bé ...
    if pagina_constelacio_en_curs.status_code == 200 :

        # "Parsegem" el contingut de la pàgina detall ...
        soup_constelacio = BeautifulSoup(pagina_constelacio_en_curs.text, 'html.parser')

        # ... localiitzem el node que conté la imatge de la constel.lació que estem tractant ...
        node_image = soup_constelacio.find("img", {"class" : "constelfigure"})

        # ... i la desem!
        desar_imatge_constelacio(node_image['src'], path_imatges, constelacio_en_curs.nom.replace(' ', '_'))

        # Ara, localitzem els nodes que contenen els diferents objectes profunds de la constel.lació en curs ...
        node_header = soup_constelacio.find("h3", text="Objetos de cielo profundo")
        node_section = node_header.parent.parent
        article_boxes_objecte_profund = node_section.findAll("div", {"class" : "articlebox"})

        # ... i iterem per ells, obtenint-ne els valors de les diferents propietats de cada objecte ...
        for article_box_objecte_profund_detall in article_boxes_objecte_profund:

            node_base_titol = article_box_objecte_profund_detall.article.header.h2
            titol_objecte_profund = node_base_titol.a.getText()

            node_base_descripcio = node_base_titol.parent.find_next('div', {"class": "articledescrip"})
            resultats = node_base_descripcio.findAll(text=True, recursive=True)

            dades_descripcio_objecte_profund = []

            # Les propietats dels objectes són text seguit amb el format "llegenda" : valor, separat per <br/>
            # A més, la propietat AR (Ascensió rectal es mesura en Hores i Minuts, separats per tags <sup> que hem de
            # manipular.
            # El bloc de codi que segueix és qui s'encarrega de tot això.

            b_ar = 0
            for resultat in resultats:
                token = str(resultat)
                if token.startswith("AR:"):
                    ar_en_curs = token
                    b_ar = 1
                else:
                    if token.startswith("Dec:"):
                        b_ar = 0
                        dades_descripcio_objecte_profund.append(ar_en_curs)
                        dades_descripcio_objecte_profund.append(token)
                    else:
                        if (b_ar == 1):
                            if (token.startswith("h")):
                                ar_en_curs = ar_en_curs + token + " "
                            else:
                                ar_en_curs = ar_en_curs + token
                        else:
                            dades_descripcio_objecte_profund.append(token)

            # Creem un element de tipus ObjecteProfund amb la informació parsejada
            objecte_profund_en_curs = ObjecteProfund(titol_objecte_profund,dades_descripcio_objecte_profund, constelacio_en_curs.nom)

            # Traça per pantalla de l'objecte ObjecteProfund en curs ...
            objecte_profund_en_curs.printObjecteProfund()

            # ... i el desem en una llista per la seva posterior iteració ...
            llista_objectes_espai_profund.append(objecte_profund_en_curs)
    else:
        print ("Error carregant pàgina: {0}.\nHTTP codi retornat: {}".format(url, pagina_constelacio_en_curs.status_code))

    # Calculem el temps que hem trigat en resoldre la petició ...
    response_delay = time.time() - t0
    # ... i ens esperem 10x l temps trigat per evitar problemes al servidor i/o que ens "bannegin" per masses crides seguides
    # interpretables com un atack de denegació de servei (DoS)
    time.sleep(10 * response_delay)

    # Codi per acotar els elements a tractar (5) durant el desenvolupament.
    # El deixem a efectes il.lustratius
    if (len(llista_constelacions) == 5):
        #break
        pass

# Finalment, escrivim el dataset amb la col.leció d'objectes llegits i enllistats ...
writeDataset((path_dataset +'objectes_profunds.csv'), header_dataset,llista_objectes_espai_profund)

# Traça de finalització
print("Web scraping finalitzat")

