import sys
from pathlib import Path
import bill_scrape

PROJECT_FOLDER = Path.cwd().parent # should this be globally defined in every module, or is one enough? read on scopes

# starteia a porra toda, chamando a busca de playbill
if len(sys.argv) > 1:
     show = "+".join(sys.argv[1:])
     show, show_url, indice = bill_scrape.find_site(show, 0)
else:
    file_CSV = open(f"{PROJECT_FOLDER}/CSV-file.txt", "r").read()
    show_list = file_CSV.split("\n")

    for i in show_list:
        show = i
        show, show_url, indice = bill_scrape.find_site(show, 0)

bill_scrape.find_playbill(show, show_url, indice)

# adicionar outros módulos e funções