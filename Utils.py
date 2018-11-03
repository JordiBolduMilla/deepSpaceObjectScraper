# Fitxer amb mètodes 'helpers'

import csv
import requests

# Funció auxiliar per escriure una llista d'objectes dins un fitxer en format CSV (dataset), delimitat per ';'
# i codificat en UTF-8
# ----------------------
# Paràmetres (per ordre)
# ----------------------
# - el nom del fitxer CSV (dataset)
# - la capçalera dels diferents valors que es desaran en el fitxer CSV
# - la llista d'objectes a desar en el fitxer

def writeDataset(dataset_file_name, headers_dataset, llista_objectes_a_serialitzar):
    with open(dataset_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        objectes_writer = csv.writer(csvfile, delimiter=';')
        objectes_writer.writerow(headers_dataset)
        for objecte_en_curs in llista_objectes_a_serialitzar:
            objectes_writer.writerow(objecte_en_curs)


# Funció auxiliar que recupera el contingut d'una petició url d'una imatge (una constel.lació)
# i la desa a la ruta indicada
# ----------------------
# Paràmetres (per ordre)
# ----------------------
# - La petició que retorna la imatge
# - La ruta on volem desar la imatge
# - El nom del fitxer que contindrà la imatge

def desar_imatge_constelacio (source_url, path_on_desar, nom_constelacio):
    the_real_url_image = getRealUrlFromImage(source_url)
    r = requests.get(the_real_url_image, stream = True)
    if r.status_code == 200 :
        aExtensio = the_real_url_image.split('.')
        ruta_imatge = path_on_desar + nom_constelacio + "." + aExtensio[len (aExtensio) - 1]
        serializeImageFromUrl(r, ruta_imatge)
    else:
        print("Error carregant imatge: {0}.\nHTTP codi retornat: {}".format(source_url, r.status_code))


# Funció auxiliar per obtenir la url REAL de la imatge que es vol descarregar
# Aquesta url és un paràmetre passat per QueryString a la cadena 'source_url'
# ----------------------
# Paràmetres (per ordre)
# ----------------------
# - La url que conté, com a paràmetre 'src', la url REAL de la imatge que volem obtenir, passada per QueryString

def getRealUrlFromImage(source_url):
    replacements = ('src=', '&')
    for r in replacements:
        source_url = source_url.replace(r, ' ')

    source_url_split = source_url.split()
    real_url_image = source_url_split[1]
    return real_url_image


# Funció auxiliar per escriure el contingut d'una petició (request) que retorna
# diferents 'chunks' binaris en un únic fitxer
# ----------------------
# Paràmetres (per ordre)
# ----------------------
# - La petició que retorna 'chunks' binaris
# - La ruta i nom del fitxer on volem desar el resultat de la petició

def serializeImageFromUrl(request, ruta):
    output = open(ruta, "wb")
    for chunk in request:
        output.write(chunk)
    output.close()


