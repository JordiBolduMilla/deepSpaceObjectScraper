import csv
import requests

def writeDataset(dataset_file_name, headers_dataset, llista_objectes_a_serialitzar):
    with open(dataset_file_name, 'w', newline='', encoding='utf-8') as csvfile:
        objectes_writer = csv.writer(csvfile, delimiter=';')
        objectes_writer.writerow(headers_dataset)
        for objecte_en_curs in llista_objectes_a_serialitzar:
            objectes_writer.writerow(objecte_en_curs)


def getRealUrlFromImage(source_url):
    replacements = ('src=', '&')
    for r in replacements:
        source_url = source_url.replace(r, ' ')

    source_url_split = source_url.split()
    real_url_image = source_url_split[1]
    return real_url_image

def serializeImageFromUrl(request, ruta):
    output = open(ruta, "wb")
    for chunk in request:
        output.write(chunk)
    output.close()

