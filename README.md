# PAC 1 : Web Scraping 

*** En construcció ***

## Descripció ##

El projecte de Web Scraping consisteix en navegar per la pàgina web http://atlasdeastronomia.com/constelaciones, extreure el llistat de constel.lacions i, a partir de cada una d'aquestes, accedir a la seva respectiva pàgina web per obenir les dades dels anomenats "Objetos de cielo profundo" (o "deep space objects")

Les dades obtingudes per cada "deep space object" (afegint el nom de la constel.lació on estan situats i que obtenim de la pàgina d'on provenim) és la informació què desem al dataset i que, segueix el següent format (exemple)

- nom : PK65-5.1/He1-6
- codi catalogacio 1 : PK65-5.1
- codi catalogacio 2 : He1-6
- magnitud : 14.9
- tipus : Nebulosa Planetaria 3(2)
- tamany : 24.0s
- ascencio rectal (AR) : 20h 17.3m
- declinació : 25º22'
- constelacio : Vulpecula


El projecte 'deepSpaceObjectScraper' consta de 2 carpetes:

- ***src***: conté el codi Pyhon per a generar el Dataset en format CSV
- ***dataset***: conté el fitxer CSV generat
