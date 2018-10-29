import csv
import time
from Constelacio import Constelacio
from ObjecteProfund import ObjecteProfund
import requests
from bs4 import BeautifulSoup

url_site = "http://atlasdeastronomia.com/"
url_site_constelacions = url_site + "constelaciones"

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

    soup_constelacio = BeautifulSoup(pagina_constelacio_en_curs.text, 'html.parser')
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

    response_delay = time.time() - t0
    time.sleep(10 * response_delay)

    if (len(llista_constelacions) == 5):
        # break
        pass


with open('objectes_profunds.csv', 'w', newline='',encoding='utf-8') as csvfile:
    objectesProfundsWriter = csv.writer(csvfile, delimiter=';')
    for objecte_profund_en_curs in llista_objectes_espai_profund:
        objectesProfundsWriter.writerow(objecte_profund_en_curs)

print("End!")
