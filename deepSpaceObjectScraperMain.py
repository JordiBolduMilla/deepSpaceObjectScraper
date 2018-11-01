import time
import os
import requests
from Constelacio import Constelacio
from ObjecteProfund import ObjecteProfund
from bs4 import BeautifulSoup
from Utils import writeDataset, getRealUrlFromImage, serializeImageFromUrl

def desar_imatge_constelacio (source_url, path_on_desar, nom_constelacio):
    the_real_url_image = getRealUrlFromImage(source_url)
    r = requests.get(the_real_url_image, stream = True)
    if r.status_code == 200 :
        aExtensio = the_real_url_image.split('.')
        ruta_imatge = path_on_desar + nom_constelacio + "." + aExtensio[len (aExtensio) - 1]
        serializeImageFromUrl(r, ruta_imatge)
    else:
        print("Error carregant imatge: {0}.\nHTTP codi retornat: {}".format(source_url, r.status_code))


print("Iniciant web scraping ...")

url_site = "http://atlasdeastronomia.com/"
url_site_constelacions = url_site + "constelaciones"
path_dataset = os.getcwd() + "/dataset/"
path_imatges = os.getcwd() + "/img/"
header_dataset= ['nom_complert_objecte','codi_catalogacio_1','codi_catalogacio_2','magnitud',
                 'tipus_objecte','tamany','ascensio_rectal','declinacio','constelacio']

# ngc, ic

pagina_ppal = requests.get(url_site_constelacions)

llista_constelacions = []
llista_objectes_espai_profund = []

soup = BeautifulSoup(pagina_ppal.text, 'html.parser')
article_boxes_constelacions = soup.findAll("div", {"class" : "articlebox"})

for article_box_constelacio in article_boxes_constelacions:

    node_base = article_box_constelacio.article
    nom = node_base.find_next('div', {"class": "articledescrip"}).getText()
    url = url_site + node_base.header.h2.a['href']

    constelacio_en_curs = Constelacio(nom, url)
    llista_constelacions.append(constelacio_en_curs)
    constelacio_en_curs.printConstelacioEnPantalla()

    t0 = time.time()
    pagina_constelacio_en_curs = requests.get(url)

    if pagina_constelacio_en_curs.status_code == 200 :

        soup_constelacio = BeautifulSoup(pagina_constelacio_en_curs.text, 'html.parser')
        node_image = soup_constelacio.find("img", {"class" : "constelfigure"})

        desar_imatge_constelacio(node_image['src'], path_imatges, constelacio_en_curs.nom.replace(' ', '_'))

        node_header = soup_constelacio.find("h3", text="Objetos de cielo profundo")
        node_section = node_header.parent.parent
        article_boxes_objecte_profund = node_section.findAll("div", {"class" : "articlebox"})

        for article_box_objecte_profund_detall in article_boxes_objecte_profund:

            node_base_titol = article_box_objecte_profund_detall.article.header.h2
            titol_objecte_profund = node_base_titol.a.getText()

            node_base_descripcio = node_base_titol.parent.find_next('div', {"class": "articledescrip"})
            resultats = node_base_descripcio.findAll(text=True, recursive=True)

            dades_descripcio_objecte_profund = []
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

            objecte_profund_en_curs = ObjecteProfund(titol_objecte_profund,dades_descripcio_objecte_profund, constelacio_en_curs.nom)
            objecte_profund_en_curs.printObjecteProfund()
            llista_objectes_espai_profund.append(objecte_profund_en_curs)
    else:
        print ("Error carregant pàgina: {0}.\nHTTP codi retornat: {}".format(url, pagina_constelacio_en_curs.status_code))

    response_delay = time.time() - t0
    time.sleep(10 * response_delay)

    if (len(llista_constelacions) == 5):
        #break
        pass

writeDataset((path_dataset +'objectes_profunds.csv'), header_dataset,llista_objectes_espai_profund)

print("Web scraping finalitzat")

